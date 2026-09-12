"""Customer customizations for Lutech (Algeria + métier opticien/clinique).

Only adds fields that do NOT already exist in ERPNext v16.
Reuses standard: customer_type, customer_group, tax_id (not duplicated).
"""

from __future__ import annotations

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter


def setup_customer():
	create_custom_fields(get_customer_custom_fields(), ignore_validate=True, update=True)
	apply_property_setters()
	ensure_customer_groups()


def get_customer_custom_fields() -> dict:
	return {
		"Customer": [
			# --- Generals: Prénom / Nom (saisie libre; standard first_name/last_name are hidden RO) ---
			{
				"fieldname": "custom_lutech_generals_section",
				"fieldtype": "Section Break",
				"label": "Generals",
				"insert_after": "customer_name",
			},
			{
				"fieldname": "custom_prenom",
				"label": "Prénom",
				"fieldtype": "Data",
				"reqd": 1,
				"insert_after": "custom_lutech_generals_section",
				"bold": 1,
			},
			{
				"fieldname": "custom_nom_famille",
				"label": "Nom de Famille",
				"fieldtype": "Data",
				"reqd": 1,
				"insert_after": "custom_prenom",
				"bold": 1,
			},
			{
				"fieldname": "custom_lutech_generals_col",
				"fieldtype": "Column Break",
				"insert_after": "custom_nom_famille",
			},
			# --- Legal & Tax & Banking tab ---
			{
				"fieldname": "custom_lutech_legal_tab",
				"fieldtype": "Tab Break",
				"label": "Legal & Tax & Banking Information",
				"insert_after": "image",
			},
			{
				"fieldname": "custom_lutech_legal_section",
				"fieldtype": "Section Break",
				"label": "Legal & Tax",
				"insert_after": "custom_lutech_legal_tab",
			},
			{
				"fieldname": "custom_nif",
				"label": "NIF",
				"fieldtype": "Data",
				"insert_after": "custom_lutech_legal_section",
				"in_list_view": 1,
				"in_standard_filter": 1,
				"translatable": 0,
			},
			{
				"fieldname": "custom_nis",
				"label": "NIS",
				"fieldtype": "Data",
				"insert_after": "custom_nif",
				"in_list_view": 1,
				"in_standard_filter": 1,
				"translatable": 0,
			},
			{
				"fieldname": "custom_lutech_legal_col",
				"fieldtype": "Column Break",
				"insert_after": "custom_nis",
			},
			{
				"fieldname": "custom_rc",
				"label": "RC (Trade Register)",
				"fieldtype": "Data",
				"insert_after": "custom_lutech_legal_col",
				"in_list_view": 1,
				"in_standard_filter": 1,
				"translatable": 0,
			},
			{
				"fieldname": "custom_ai",
				"label": "AI (Tax Article)",
				"fieldtype": "Data",
				"insert_after": "custom_rc",
				"translatable": 0,
			},
			{
				"fieldname": "custom_lutech_banking_section",
				"fieldtype": "Section Break",
				"label": "Banking",
				"insert_after": "custom_ai",
			},
			{
				"fieldname": "custom_rib",
				"label": "RIB",
				"fieldtype": "Data",
				"insert_after": "custom_lutech_banking_section",
				"in_list_view": 1,
				"in_standard_filter": 1,
				"translatable": 0,
			},
			{
				"fieldname": "custom_bank_name",
				"label": "Bank Name",
				"fieldtype": "Data",
				"insert_after": "custom_rib",
				"translatable": 0,
			},
			{
				"fieldname": "custom_lutech_banking_col",
				"fieldtype": "Column Break",
				"insert_after": "custom_bank_name",
			},
			{
				"fieldname": "custom_ccp",
				"label": "CCP",
				"fieldtype": "Data",
				"insert_after": "custom_lutech_banking_col",
				"in_list_view": 1,
				"in_standard_filter": 1,
				"translatable": 0,
			},
			{
				"fieldname": "custom_cle",
				"label": "Clé",
				"fieldtype": "Data",
				"insert_after": "custom_ccp",
				"translatable": 0,
			},
			# --- Contact tab (standard contact fields remain; tab groups them visually) ---
			{
				"fieldname": "custom_lutech_contact_tab",
				"fieldtype": "Tab Break",
				"label": "Contact & responsible",
				"insert_after": "custom_cle",
			},
		]
	}


def apply_property_setters():
	"""Reuse standard fields with PM labels — do not duplicate customer_type / customer_group."""
	make_property_setter(
		"Customer",
		"customer_type",
		"label",
		"Legal type",
		"Data",
		validate_fields_for_doctype=False,
	)
	make_property_setter(
		"Customer",
		"customer_group",
		"label",
		"Catégorie",
		"Data",
		validate_fields_for_doctype=False,
	)
	make_property_setter(
		"Customer",
		"customer_group",
		"reqd",
		"1",
		"Check",
		validate_fields_for_doctype=False,
	)
	# Auto-filled from Prénom + Nom de Famille
	make_property_setter(
		"Customer",
		"customer_name",
		"read_only",
		"1",
		"Check",
		validate_fields_for_doctype=False,
	)


def ensure_customer_groups():
	"""Seed métier categories used as Customer Group (Catégorie)."""
	parent = "All Customer Groups"
	if not frappe.db.exists("Customer Group", parent):
		# Site may lack setup-wizard fixtures (empty Customer Group tree).
		frappe.get_doc(
			{
				"doctype": "Customer Group",
				"customer_group_name": parent,
				"is_group": 1,
				"parent_customer_group": "",
			}
		).insert(ignore_permissions=True)

	for group_name in ("Optician", "Clinic"):
		if frappe.db.exists("Customer Group", group_name):
			continue
		doc = frappe.get_doc(
			{
				"doctype": "Customer Group",
				"customer_group_name": group_name,
				"parent_customer_group": parent,
				"is_group": 0,
			}
		)
		doc.insert(ignore_permissions=True)
