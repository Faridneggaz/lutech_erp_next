"""Hide desk workspaces except Selling, Buying and Stock.

Uses Desktop Icon.hidden and Workspace.is_hidden — not User / Module Profile.
"""

from __future__ import annotations

import frappe

ALLOWED = {"Selling", "Buying", "Stock"}


def setup_desk_visibility():
	"""Hide every desktop icon and public workspace except Selling, Buying, Stock."""
	_hide_desktop_icons()
	_hide_workspaces()
	_clear_user_module_profiles()
	frappe.clear_cache()
	return _summary()


def _hide_desktop_icons():
	icons = frappe.get_all("Desktop Icon", fields=["name", "label", "hidden"])
	for icon in icons:
		should_hide = 0 if icon.label in ALLOWED else 1
		if int(icon.hidden or 0) != should_hide:
			frappe.db.set_value(
				"Desktop Icon",
				icon.name,
				"hidden",
				should_hide,
				update_modified=False,
			)


def _hide_workspaces():
	workspaces = frappe.get_all(
		"Workspace",
		filters={"public": 1},
		fields=["name", "is_hidden"],
	)
	for workspace in workspaces:
		should_hide = 0 if workspace.name in ALLOWED else 1
		if int(workspace.is_hidden or 0) != should_hide:
			frappe.db.set_value(
				"Workspace",
				workspace.name,
				"is_hidden",
				should_hide,
				update_modified=False,
			)


def _clear_user_module_profiles():
	"""Undo the previous User Module Profile approach."""
	users = frappe.get_all("User", filters={"module_profile": ["is", "set"]}, pluck="name")
	for user in users:
		frappe.db.set_value("User", user, "module_profile", None, update_modified=False)
		frappe.db.delete("Block Module", {"parent": user, "parenttype": "User"})

	if frappe.db.exists("Module Profile", "Lutech Sell Buy Stock"):
		frappe.delete_doc(
			"Module Profile",
			"Lutech Sell Buy Stock",
			ignore_permissions=True,
			force=True,
		)


def _summary():
	visible_icons = frappe.get_all(
		"Desktop Icon",
		filters={"hidden": 0},
		pluck="label",
		order_by="label asc",
	)
	visible_workspaces = frappe.get_all(
		"Workspace",
		filters={"public": 1, "is_hidden": 0},
		pluck="name",
		order_by="name asc",
	)
	return {
		"visible_icons": visible_icons,
		"visible_workspaces": visible_workspaces,
	}
