"""Desk module visibility for Lutech.

Keeps only Selling, Buying and Stock visible; blocks every other module.
Applies to every System User (existing + new).
"""

from __future__ import annotations

import frappe
from frappe.utils.modules import get_modules_from_all_apps

PROFILE_NAME = "Lutech Sell Buy Stock"
ALLOWED_MODULES = {"Selling", "Buying", "Stock"}


def setup_module_profile(apply_to_users: bool = True):
	"""Create/update Module Profile and assign it to all System Users."""
	all_modules = sorted({m.get("module_name") for m in get_modules_from_all_apps() if m.get("module_name")})
	blocked = [m for m in all_modules if m not in ALLOWED_MODULES]

	if frappe.db.exists("Module Profile", PROFILE_NAME):
		doc = frappe.get_doc("Module Profile", PROFILE_NAME)
		doc.set("block_modules", [])
	else:
		doc = frappe.new_doc("Module Profile")
		doc.module_profile_name = PROFILE_NAME

	for module in blocked:
		doc.append("block_modules", {"module": module})

	doc.flags.ignore_permissions = True
	doc.save()

	if apply_to_users:
		_apply_profile_to_all_system_users(PROFILE_NAME)

	frappe.clear_cache()
	return PROFILE_NAME, blocked


def _apply_profile_to_all_system_users(profile_name: str):
	"""Assign profile to every System User except Guest."""
	users = frappe.get_all(
		"User",
		filters={
			"enabled": 1,
			"user_type": "System User",
			"name": ("not in", ("Guest",)),
		},
		pluck="name",
	)
	for user_name in users:
		_assign_profile_to_user(user_name, profile_name)


def _assign_profile_to_user(user_name: str, profile_name: str):
	user = frappe.get_doc("User", user_name)
	changed = user.module_profile != profile_name
	user.module_profile = profile_name
	user.validate_allowed_modules()
	user.flags.ignore_permissions = True
	user.save()
	return changed


def on_user_validate(doc, method=None):
	"""Force Lutech module profile on every System User (all profiles/users)."""
	if doc.name in ("Guest",) or doc.user_type != "System User":
		return
	if not frappe.db.exists("Module Profile", PROFILE_NAME):
		return
	if doc.module_profile != PROFILE_NAME:
		doc.module_profile = PROFILE_NAME
	# Sync block_modules from profile whenever user is saved
	if doc.module_profile == PROFILE_NAME:
		doc.validate_allowed_modules()
