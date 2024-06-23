# -*- coding: utf-8 -*-
{
    'name': "Gulf Tunneling Company",

    'summary': """
        GTC """,

    'description': """
        GTC.
    """,

    'author': "MetaData",
    'website': "https://metadatauae.com",

    'category': 'General',

    # any module necessary for this one to work correctly
    'depends': ['hr_expense','purchase_requisition','hr','project',
                'rfq_separate_sequence','hr_department_user', 'hr_maintenance', 'account'
                ],

    # always loaded
    'data': [
        'security/security.xml',
        	
	'views/project_view.xml',
        'views/purchase.xml',
        'views/product.xml',
        'views/partner.xml',
	'views/stock.xml',
	'views/maintenance.xml',
	'views/expenses.xml',
        'views/account.xml',

        'reports/paperformat.xml',
	'reports/internal_layout.xml',
        'reports/expense_statement.xml',
        'reports/report_receipt_voucher.xml',
        'reports/report_release_voucher.xml',
	'reports/report_wo_request.xml',
        'reports/po_report.xml',
        'reports/pr_report.xml',
	'reports/qtn_comparison.xml',
	'reports/pm_report.xml',
        'reports/pm_summary_report.xml'

    ],

    'installable': True,
    'application': True,
    'auto_install': True,
}
