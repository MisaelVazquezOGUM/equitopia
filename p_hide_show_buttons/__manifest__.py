# -*- coding: utf-8 -*-
# Part of Param Enterprice. See LICENSE file for full copyright and licensing details.
{
    'name': "Hide/Show Buttons",
    'summary': "Hide/Show Buttons for particular Users for Selected Views and Models",
    'description': "Hide/Show Buttons for particular Users for Selected Views and Models",
    "version": "0.1",
    'price': 10,
    'currency': 'EUR',
    "category": "Other",
    'author': "Param Enterprice",
    'license': 'Other proprietary',
    'images': ['static/description/image.png'],
    "depends": [
        'web','base'
    ],
    "data": [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/res_users_view.xml',
        'views/templates.xml',
    ],
    "application": False,
    'installable': True,
}
