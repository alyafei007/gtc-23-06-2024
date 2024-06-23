# -*- coding: utf-8 -*-
{
    'name': "HR Department User",

    'summary': """
        HR Department User """,

    'description': """
        HR Department User.
    """,

    'author': "MetaData",
    'website': "https://metadatauae.com",

    'category': 'General',

    # any module necessary for this one to work correctly
    'depends': ['hr'],

    # always loaded
    'data': [
    'views/hr_department.xml',
    ],

    'installable': True,
    'application': False,
    'auto_install': False,
}
