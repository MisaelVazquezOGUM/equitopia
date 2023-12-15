# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2021-Present NegblaSoft- Adrex Gom & Luigi Tolayo
#     (<>).
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Tablero Power BI',
    'version': '1.0',
    'depends': [
            'base',
            'custom_property_fields_add'
    ],
    'license': 'Other proprietary',
    'price': 9999.0,
    'category': 'Sales',
    'currency': 'MXN',
    'summary': """NegblaSoftCustom module""",
    'description': "",
    'author': 'Adrex Gom & Luigi Tolayo',
    'support': 'tolayoluigi@gmail.com',
    #'assets': {
    #    'web.assets_backend': [
    #        '/board_power_bi_v13/static/description/src/power_bi.css',
    #    ],
    #},
    
    'data': [
        'views/views.xml',
    ],
    
    "application"           : True,
    "installable"           : True,
    "auto_install"          : False,
}


