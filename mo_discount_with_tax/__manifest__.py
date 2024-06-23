# -*- coding: utf-8 -*-
{
    'name': "Invoice Discount with Tax Calculation",
    'version': '14.0.0',
    'category': 'Sales',

    'summary': """
        Invoice discount with and without tax amount""",

    'description': """
        This module have global discount on sales order and Invoice	
    """,

    'author': "Tifan Technology",
    'website': "https://www.tifan.ae",


    # any module necessary for this one to work correctly
    'depends': ['base','sale','sale_management','account','stock'],

    # always loaded
    'data': [
	'views/sale_view.xml',
        'report/inherit_sale_report.xml',
        'report/inherit_account_report.xml'
	],
    'installable': True,
    'auto_install': False,
    'application': True,
    'images':['static/description/Banner.png'],
}
