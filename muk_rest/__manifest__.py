# -*- coding: utf-8 -*-

###################################################################################
# 
#    Copyright (C) 2017 MuK IT GmbH
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###################################################################################

{
    "name": "REST API",
    "summary": """Restful API for Odoo""",
    "description": """ 
        Enables a REST API for the Odoo server. The API has
        routes to authenticate and retrieve a token. Afterwards,
        a set of routes to interact with the server are provided.
        A documentation about every available route can be found
        inside the README file.
    """,
    "version": "10.0.1.0.0",
    "category": "Extra Tools",
    "license": "OPL-1",
    "price": 45.00,
    "currency": 'EUR',
    "website": "http://www.mukit.at",
    "author": "MuK IT",
    "contributors": [
        "Mathias Markl <mathias.markl@mukit.at>",
    ],
    "depends": [
        "base",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/rest_menu.xml",
        "views/rest_token_view.xml",
    ],
    "demo": [
    ],
    "qweb": [
        "static/src/xml/*.xml",
    ],
    "images": [
        'static/description/banner.png'
    ],
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "application": False,
    "installable": True,
    "auto_install": False,
    
}
