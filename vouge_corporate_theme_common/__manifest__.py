# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Bizople Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    # Theme information
    'name': 'Vouge Corporate Theme Common',
    'category': 'Website',
    'version': '13.0.0.2',
    'author': 'Bizople Solutions Pvt. Ltd.',
    'website': 'https://www.bizople.com',
    'summary': 'Vouge Corporate Theme Common',
    'description': """Vouge Corporate Theme Common""",
    'depends': [
        'website',
        'website_crm',
        'website_blog',
        'mass_mailing',
        'portal',
        'theme_default',
        'web_editor',
    ],

    'data': [
            'security/ir.model.access.csv',
            'data/data.xml',
            'views/dynamicslider.xml',
            'views/res_config.xml',
            'views/slider_snippets.xml',
            'views/newsletter_popup_inherit.xml',
            'views/portal_template.xml',
            'views/help_center_template.xml',
            'views/blog_page_inherit.xml',

            'views/cookie_policy_view.xml',
            'views/cookie_template.xml',
            
            #Headers
            'views/headers/header_template1.xml',
            'views/headers/header_template2.xml',
            'views/headers/header_template3.xml',
            'views/headers/header_template4.xml',
            'views/headers/header_template5.xml',
            'views/headers/header_template6.xml',
    ],

    'images': [
        'static/description/banner.jpg'
    ],


    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'OPL-1',
    'price': 20,
    'currency': 'EUR',
}
