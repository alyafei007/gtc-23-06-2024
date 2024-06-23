# -*- encoding: utf-8 -*-
{
    'name' : 'Report For BID EVALUATION',
    'version' : '14.0.1.0.0',
    'category' : 'Purchase Requisition',
    'author' : 'Premananth',
    'website' : 'https://www.metadatauae.com',
    'summary': """Report For BID EVALUATION""",
    'depends' : ['base_setup', 'purchase_requisition'],
    'data': [
        'security/ir.model.access.csv',
        'views/report.xml',
        'views/bid_evaluation_template_v1.xml',
        'views/report_purchase_requisition_excel_view.xml',
    ],    
    'installable': True,
    'auto_install': False,
}