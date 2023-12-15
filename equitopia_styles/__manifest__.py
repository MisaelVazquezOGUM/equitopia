###################################################################################
#
#    Copyright (c) 2017-2019 MuK IT GmbH.
#
#    This file is part of MuK Backend Theme 
#    (see https://mukit.at).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>. 
#  
###################################################################################
{
    "name": "Equitopia Styles", 
    "summary": "Odoo Community Backend Theme",
    "version": "13.0.1.0.6", 
    "category": "Themes/Backend",
    "author": "OGUM",
    "website": "https://intranet.ogum.com.mx/",
    "contributors": [
        "OGUM",
    ],
    "depends": [
        "website",
        "muk_web_theme",
        "muk_web_theme_mail",
    ],
    "excludes": [
        "web_enterprise",
    ],
    "data": [
        "template/assets.xml",
        # "template/web.xml",
        # "views/res_users.xml",
        # "views/res_config_settings_view.xml",
        # "data/res_company.xml",
    ],
    "images": [
        'static/description/banner.png',
        'static/description/theme_screenshot.png'
    ],
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "application": False,
    "installable": True,
    "auto_install": False,
    # "uninstall_hook": "_uninstall_reset_changes",
}
