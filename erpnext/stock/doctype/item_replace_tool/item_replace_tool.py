# Copyright (c) 2022, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import get_link_to_form


class ItemReplaceTool(Document):
	pass


class ItemReplacer:
	def __init__(self, old_item_code: str, new_item_code: str, update_stock: bool = True) -> None:
		self.old_item = frappe.get_doc("Item", old_item_code)
		self.new_item = frappe.get_doc("Item", new_item_code)
		self.update_stock = update_stock

	def replace(self) -> None:
		self._check_if_replacable()
		self._ensure_no_transaction_on_new_item()
		if self.update_stock:
			self._replace_stock()
		self._disable_old_item()

	def _check_if_replacable(self):
		meta = frappe.get_meta("Item")
		same_properties = (
			"is_stock_item",
			"include_item_in_manufacturing",
			"has_serial_no",
			"has_batch_no"
		)
		for prop in same_properties:
			if self.old_item.get(prop) != self.new_item.get(prop):
				frappe.throw(_("The value of {} must be same for both items.").format(meta.get_label(prop)))

	def _ensure_no_transaction_on_new_item(self):
		if frappe.db.count("Stock Ledger Entry", {"item_code": self.new_item.name, "is_cancelled": 0}):
			frappe.throw(_("Can not replace items since new item has Stock transactions against it."))

	def _replace_stock(self):
		"""Create stock reconciliation that moves item's inventory and value from old item to new item."""
		pass

	def _disable_old_item(self):
		self.old_item.disabled = 1
		replace_message = _("This Item has been replaced by {}").format(get_link_to_form(self.new_item.doctype, self.new_item.name))
		self.old_item.add_comment(text=replace_message)
		self.old_item.save()



def replace_item(old: str, new: str) -> None:
	replacer = ItemReplacer(old, new)
	replacer.replace()
