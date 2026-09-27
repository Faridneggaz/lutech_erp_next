#!/usr/bin/env python3
"""Generate PDF documentation of Customer field customizations for Lutech."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
	Paragraph,
	SimpleDocTemplate,
	Spacer,
	Table,
	TableStyle,
	KeepTogether,
)

OUT = Path(__file__).resolve().parent / "Lutech_Customer_Fields.pdf"

BRAND = colors.HexColor("#0B3D5C")
ACCENT = colors.HexColor("#1A6B8A")
LIGHT = colors.HexColor("#F4F7FA")
HEADER_BG = colors.HexColor("#0B3D5C")
GREEN = colors.HexColor("#1B6B3A")
ORANGE = colors.HexColor("#9A5B00")
BLUE = colors.HexColor("#0B4F8A")


def styles():
	base = getSampleStyleSheet()
	return {
		"title": ParagraphStyle(
			"TitleFR",
			parent=base["Title"],
			fontSize=18,
			textColor=BRAND,
			spaceAfter=6,
			alignment=TA_CENTER,
			fontName="Helvetica-Bold",
		),
		"subtitle": ParagraphStyle(
			"SubFR",
			parent=base["Normal"],
			fontSize=10,
			textColor=ACCENT,
			spaceAfter=16,
			alignment=TA_CENTER,
		),
		"h1": ParagraphStyle(
			"H1FR",
			parent=base["Heading1"],
			fontSize=13,
			textColor=BRAND,
			spaceBefore=14,
			spaceAfter=8,
			fontName="Helvetica-Bold",
		),
		"body": ParagraphStyle(
			"BodyFR",
			parent=base["Normal"],
			fontSize=9,
			leading=12,
			textColor=colors.HexColor("#222222"),
			spaceAfter=6,
		),
		"cell": ParagraphStyle(
			"CellFR",
			parent=base["Normal"],
			fontSize=8,
			leading=10,
			textColor=colors.HexColor("#222222"),
		),
		"cell_header": ParagraphStyle(
			"CellHdr",
			parent=base["Normal"],
			fontSize=8,
			leading=10,
			textColor=colors.white,
			fontName="Helvetica-Bold",
		),
		"footer": ParagraphStyle(
			"FooterFR",
			parent=base["Normal"],
			fontSize=8,
			textColor=colors.gray,
			alignment=TA_CENTER,
		),
	}


def P(text, style):
	return Paragraph(text.replace("\n", "<br/>"), style)


def make_table(headers, rows, col_widths, s):
	data = [[P(h, s["cell_header"]) for h in headers]]
	for row in rows:
		data.append([P(str(c), s["cell"]) for c in row])
	t = Table(data, colWidths=col_widths, repeatRows=1)
	t.setStyle(
		TableStyle(
			[
				("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
				("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
				("BACKGROUND", (0, 1), (-1, -1), LIGHT),
				("ROWBACKGROUNDS", (0, 1), (-1, -1), [LIGHT, colors.white]),
				("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#C5D0DA")),
				("VALIGN", (0, 0), (-1, -1), "TOP"),
				("LEFTPADDING", (0, 0), (-1, -1), 5),
				("RIGHTPADDING", (0, 0), (-1, -1), 5),
				("TOPPADDING", (0, 0), (-1, -1), 4),
				("BOTTOMPADDING", (0, 0), (-1, -1), 4),
			]
		)
	)
	return t


def build():
	s = styles()
	doc = SimpleDocTemplate(
		str(OUT),
		pagesize=A4,
		leftMargin=1.5 * cm,
		rightMargin=1.5 * cm,
		topMargin=1.5 * cm,
		bottomMargin=1.5 * cm,
		title="Lutech – Modifications champs Customer",
		author="Lutech ERP Next",
	)

	story = []
	story.append(P("Lutech ERP Next", s["title"]))
	story.append(
		P(
			"Documentation des champs Customer<br/>"
			"Ajouts · Renommages · Champs ERPNext réutilisés",
			s["subtitle"],
		)
	)
	story.append(
		P(
			"<b>DocType :</b> Customer &nbsp;|&nbsp; <b>App :</b> lutech_erp_next &nbsp;|&nbsp; "
			"<b>ERPNext :</b> v16 &nbsp;|&nbsp; <b>Date :</b> septembre 2026",
			s["body"],
		)
	)
	story.append(
		P(
			"Principe : n’ajouter que les champs absents d’ERPNext. "
			"Réutiliser les champs standards (<b>customer_type</b>, <b>customer_group</b>, "
			"<b>tax_id</b>, <b>customer_name</b>) via Property Setter / logique, sans duplication.",
			s["body"],
		)
	)

	# --- Section 1: Added fields ---
	story.append(P("1. Champs ajoutés (Custom Fields)", s["h1"]))
	story.append(
		P(
			"Ces champs sont créés par <b>lutech_erp_next</b> (préfixe <b>custom_</b>). "
			"Ils n’existent pas dans ERPNext standard.",
			s["body"],
		)
	)

	added = [
		["custom_lutech_generals_section", "Generals", "Section Break", "Après customer_name — section Prénom/Nom"],
		["custom_prenom", "Prénom", "Data (obligatoire)", "Saisie libre ; alimente customer_name"],
		["custom_nom_famille", "Nom de Famille", "Data (obligatoire)", "Saisie libre ; alimente customer_name"],
		["custom_lutech_generals_col", "—", "Column Break", "Mise en page colonne"],
		["custom_lutech_legal_tab", "Legal & Tax & Banking Information", "Tab Break", "Nouvel onglet légal / banque"],
		["custom_lutech_legal_section", "Legal & Tax", "Section Break", "Bloc fiscal Algérie"],
		["custom_nif", "NIF", "Data", "Numéro d’Identification Fiscale — liste + filtre"],
		["custom_nis", "NIS", "Data", "Numéro d’Identification Statistique — liste + filtre"],
		["custom_lutech_legal_col", "—", "Column Break", "Mise en page colonne"],
		["custom_rc", "RC (Trade Register)", "Data", "Registre de commerce — liste + filtre"],
		["custom_ai", "AI (Tax Article)", "Data", "Article d’imposition"],
		["custom_lutech_banking_section", "Banking", "Section Break", "Bloc bancaire"],
		["custom_rib", "RIB", "Data", "Relevé d’Identité Bancaire — liste + filtre"],
		["custom_bank_name", "Bank Name", "Data", "Nom de la banque"],
		["custom_lutech_banking_col", "—", "Column Break", "Mise en page colonne"],
		["custom_ccp", "CCP", "Data", "Compte CCP — liste + filtre"],
		["custom_cle", "Clé", "Data", "Clé RIB / CCP"],
		["custom_lutech_contact_tab", "Contact & responsible", "Tab Break", "Onglet regroupant les contacts standards"],
	]
	story.append(
		make_table(
			["Fieldname", "Label", "Type", "Rôle"],
			added,
			[3.6 * cm, 3.8 * cm, 3.2 * cm, 6.4 * cm],
			s,
		)
	)

	# --- Section 2: Renamed / property setters ---
	story.append(P("2. Champs ERPNext renommés / modifiés (Property Setters)", s["h1"]))
	story.append(
		P(
			"Aucun nouveau champ : on change seulement le label ou le comportement "
			"d’un champ <b>déjà présent</b> dans ERPNext.",
			s["body"],
		)
	)
	renamed = [
		[
			"customer_type",
			"Customer Type → <b>Legal type</b>",
			"Label",
			"Type juridique (Company / Individual, etc.) — champ standard ERPNext",
		],
		[
			"customer_group",
			"Customer Group → <b>Catégorie</b>",
			"Label + obligatoire",
			"Catégorie métier (Optician, Clinic…) — champ standard ERPNext",
		],
		[
			"customer_name",
			"Customer Name (inchangé)",
			"Lecture seule",
			"Rempli auto = Prénom + Nom de Famille (JS + validate Python)",
		],
	]
	story.append(
		make_table(
			["Fieldname ERPNext", "Modification", "Propriété", "Détail"],
			renamed,
			[3.2 * cm, 4.2 * cm, 2.8 * cm, 6.8 * cm],
			s,
		)
	)

	# --- Section 3: Existing reused ---
	story.append(P("3. Champs ERPNext existants réutilisés (non dupliqués)", s["h1"]))
	story.append(
		P(
			"Ces champs standards existent déjà. L’app <b>ne les recrée pas</b> "
			"(pas de custom_tax_id, pas de second customer_type, etc.).",
			s["body"],
		)
	)
	existing = [
		["customer_name", "Customer Name", "Data", "Nom affiché ; calculé depuis Prénom + Nom"],
		["customer_type", "Legal type (renommé)", "Select", "Type légal standard ERPNext"],
		["customer_group", "Catégorie (renommé)", "Link → Customer Group", "Catégories Optician / Clinic ajoutées"],
		["tax_id", "Tax ID", "Data", "Identifiant fiscal standard — non dupliqué (NIF est à part)"],
		["image", "Image", "Attach Image", "Point d’insertion de l’onglet Legal"],
		["(contacts liés)", "Contact / Address", "Liens standard", "Onglet Contact & responsible les regroupe visuellement"],
	]
	story.append(
		make_table(
			["Fieldname", "Label (UI Lutech)", "Type ERPNext", "Usage Lutech"],
			existing,
			[3.2 * cm, 3.8 * cm, 3.6 * cm, 6.4 * cm],
			s,
		)
	)

	# --- Section 4: Customer groups ---
	story.append(P("4. Données de référence ajoutées (Customer Group)", s["h1"]))
	story.append(
		P(
			"Pas des champs, mais des enregistrements créés sous le champ standard "
			"<b>customer_group</b> (affiché « Catégorie ») :",
			s["body"],
		)
	)
	groups = [
		["All Customer Groups", "Groupe parent (créé si absent)", "is_group = 1"],
		["Optician", "Catégorie métier opticien", "Enfant de All Customer Groups"],
		["Clinic", "Catégorie métier clinique", "Enfant de All Customer Groups"],
	]
	story.append(
		make_table(
			["Nom", "Description", "Remarque"],
			groups,
			[4.5 * cm, 6.5 * cm, 6.0 * cm],
			s,
		)
	)

	# --- Section 5: Summary ---
	story.append(P("5. Synthèse", s["h1"]))
	summary = [
		["Custom Fields ajoutés (saisie métier)", "11 champs Data + 7 breaks/tabs/sections", "Nouveaux"],
		["Dont champs métier Algérie", "NIF, NIS, RC, AI, RIB, Bank Name, CCP, Clé", "Nouveaux"],
		["Dont identité", "Prénom, Nom de Famille", "Nouveaux (customer_name auto)"],
		["Property Setters", "customer_type, customer_group, customer_name", "Existants modifiés"],
		["Champs ERPNext non dupliqués", "customer_type, customer_group, tax_id, customer_name", "Réutilisés"],
	]
	story.append(
		make_table(
			["Catégorie", "Contenu", "Statut"],
			summary,
			[5.5 * cm, 8.5 * cm, 3.0 * cm],
			s,
		)
	)

	story.append(Spacer(1, 12))
	story.append(
		P(
			"Source : apps/lutech_erp_next/lutech_erp_next/setup/customer.py · "
			"overrides/customer.py · public/js/customer.js",
			s["footer"],
		)
	)

	doc.build(story)
	print(f"OK: {OUT}")


if __name__ == "__main__":
	build()
