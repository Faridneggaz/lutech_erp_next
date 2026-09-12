import frappe
from frappe import _


def validate(doc, method=None):
	"""Keep customer_name in sync with Prénom + Nom de Famille."""
	parts = [doc.get("custom_prenom"), doc.get("custom_nom_famille")]
	full = " ".join(p.strip() for p in parts if p and str(p).strip())
	if full:
		doc.customer_name = full
	elif not doc.customer_name:
		frappe.throw(_("Please set Prénom and Nom de Famille"))
