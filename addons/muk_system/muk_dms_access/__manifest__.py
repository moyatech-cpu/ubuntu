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
    'name': "MuK Documents Access",
    'summary': """Access Control""",
    'version': '11.0.2.0.0',   
    'category': 'Document Management',   
    'license': 'AGPL-3',    
    'author': "MuK IT",
    'website': "http://www.mukit.at",
    "live_test_url": "https://demo.mukit.at/web/login",
    'contributors': [
        "Mathias Markl <mathias.markl@mukit.at>",
    ],
    'depends': [
        'muk_dms',
    ],
    "data": [
        'views/dms_directory_view.xml',
        'views/dms_file_view.xml',
        'views/security_groups_view.xml',
    ],
    "demo": [
        "demo/dms_access_groups_demo.xml",
        "demo/dms_settings_demo.xml",
        "demo/dms_directory_demo.xml",
        "demo/dms_file_demo.xml",
    ],
    "qweb": [
        "static/src/xml/*.xml",
    ],
    'images': [
        'static/description/banner.png'
    ],
    "application": False,
    "installable": True,
}
