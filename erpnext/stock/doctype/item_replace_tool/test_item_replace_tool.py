# Copyright (c) 2022, Frappe Technologies Pvt. Ltd. and Contributors
# See license.txt

import frappe

from erpnext.stock.doctype.item_replace_tool.item_replace_tool import replace_item
from erpnext.tests.utils import ERPNextTestCase


class TestItemReplaceTool(ERPNextTestCase):

	def tearDown(self) -> None:
		frappe.db.rollback()
		return super().tearDown()

	def test_disabling_and_comments(self):
		"""Item replace tool should disable old item and leave comment"""
		old, new = create_items_for_replace()
		replace_item(old.name, new.name)
		old.reload()

		self.assertEqual(old.disabled, 1)
		comments = frappe.get_list("Comment",
				filters={
					"reference_doctype": old.doctype,
					"reference_name": old.name,
					"comment_type": "Comment"},
				fields="content"
		)
		self.assertGreaterEqual(len(comments), 1)
		self.assertIn("replaced by", comments[0].content)

	def test_update_stock_basic(self):
		old, new = create_items_for_replace()
		pass

	def test_update_stock_batched(self):
		pass

	def test_update_stock_serialized(self):
		pass


def create_items_for_replace(old_props=None, new_props=None):
	return _create_item(old_props), _create_item(new_props)

def _create_item(props=None):
	item = frappe.new_doc("Item")
	item.item_code = frappe.generate_hash(length=10)
	item.item_group = "All Item Groups"
	if props:
		item.update(props)
	return item.insert()
