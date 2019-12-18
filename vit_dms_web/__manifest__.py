# -*- coding: utf-8 -*-
{
    'name': "vit_dms_review",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://vitraining.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'vit_muk_dms',
                'website',
                'muk_dms',
                'muk_web_preview',
                'muk_dms_file',
                'muk_web_client',
                'muk_web_view_hierarchy',
                'muk_web_client_refresh',
        ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/asset.xml',
        'views/views.xml',
        'views/templates.xml',
        'data/web_menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}