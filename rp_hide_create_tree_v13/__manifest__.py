#-*- coding:utf-8 -*-
{
    'name': "RP Hide Create, Edit, Import and Export button",
    'version': '13.0.1.0.0',
    'description': "Hide create, edit, import and export button based on groups",
    'summary': 'This module helps to hide create, edit, import and export button from List, Form and Kanban view based on groups.',
    'author': '''
                - RP Odoo Developer, Rishabh Jadia, Pragya Ladda
            ''',
    'category': 'Web',
    'license': "OPL-1",
    'depends': ['web', 'base_import'],
    'data': [
        'security/groups.xml',
        'views/assets.xml',
    ],
    'qweb': [
        'static/src/xml/create_edit_btn.xml',
    ],
    'images': [
        'static/description/banner.png',
    ],
    'installable': True,
}
