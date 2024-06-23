# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name":   "EnterpriseMate Theme Config",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Extra Tools",
    "summary": "Enterprise Backend Theme, Enterprise Theme, Backend Enterprise Theme",
    "description": """
Do you want odoo enterpise look in your community version? Are You looking for modern, creative, clean, clear, materialise odoo enterpise look theme for your backend? So you are at the right place, We have made sure that this theme is highly clean, modern, fully customizable enterprise look theme. Cheers!""",
    "version": "13.0.15",
    "depends": [
        "base", "base_setup"

    ],
    "application": True,
    "data": [
        "security/base_security.xml",
        "security/ir.model.access.csv",
        "data/theme_config_data.xml",
        "views/ent_theme_config_view.xml",
        "views/assets_backend.xml",
        "views/global_search_view.xml",
        "wizard/theme_preview_wizard.xml",

    ],
    "images": ["static/description/banner.gif", ],
    "auto_install": False,
    "installable": True,
    "price": 1,
    "currency": "EUR"
}
