# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
  "name"                 :  "Odoo Maintenance Mode",
  "summary"              :  """Odoo Maintenance Mode allows to put Odoo server(both website and backend) in the maintenance mode while performing some diagnostic tests on server. It allows to prevent customer requests during maintenance mode.""",
  "category"             :  "Website",
  "version"              :  "1.0.01",
  "sequence"             :  45,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Maintenance-Mode.html",
  "description"          :  """Odoo Maintenance Mode 
Maintenance Mode in Odoo
Maintenance Mode
Odoo Under Construction
Odoo Under Construction Mode
Maintenance Module
Odoo Maintenance Module
Odoo Maintenance Mode Module
Module Under Construction
Maintenance Mode Module""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=odoo_maintenance_mode",
  "depends"              :  ['website'],
  "data"                 :  [
                             'views/maintenance_mode_view.xml',
                             'data/email_template.xml',
                             'views/res_config_view.xml',
                             'views/templates.xml',
                             'wizard/wizard_message_view.xml',
                             'security/ir.model.access.csv',
                            ],
  "demo"                 :  ['data/demo.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  69,
  "currency"             :  "USD",
  "pre_init_hook"        :  "pre_init_check",
}