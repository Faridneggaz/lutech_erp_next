// Copyright (c) 2026, Lutech and contributors
// License: MIT

frappe.ui.form.on("Customer", {
	refresh(frm) {
		set_customer_name_from_parts(frm);
	},
	custom_prenom(frm) {
		set_customer_name_from_parts(frm);
	},
	custom_nom_famille(frm) {
		set_customer_name_from_parts(frm);
	},
});

function set_customer_name_from_parts(frm) {
	const full = [frm.doc.custom_prenom, frm.doc.custom_nom_famille]
		.filter(Boolean)
		.join(" ")
		.trim();
	if (full && frm.doc.customer_name !== full) {
		frm.set_value("customer_name", full);
	}
}
