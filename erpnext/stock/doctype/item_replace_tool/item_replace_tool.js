// Copyright (c) 2022, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Item Replace Tool', {
	refresh: function(frm) {
		frm.disable_save();
	},
});
