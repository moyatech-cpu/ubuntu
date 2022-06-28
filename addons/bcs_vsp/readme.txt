name: "bcs_vsp",
summary: Module to fix the voucher value defect, compute voucher value on change, and add menu item for VP 19 form.

important files within this module
==================================
/data/mail_templates.xml
/__manifest__.py
/__init__.py
/static/description/icon.png
/static/src/img/icon.png
/models/__init__.py
/models/pitch_polish_rating.py

This update requires a change on the studio on view_submit_product_wiz_form.
view_submit_product_wiz_form: <field name="invoice_number" invisible="0"/>
view.voucher.application.form:460 <field name="invoice_number" string="Invoice Number"/>
Under voucher application, comment existing x_voucher_value and restart server

<t t-value="o.grant_bcs_vsp_data()" t-set="data_vals"/>
                            
<t t-esc="data_vals.get('priority')"/>

bcs_number
edm
bcs
date
no_vouchers
priority
sp
vouchers[
main_no
sp
vch_no
inv_no
services[service_name]
branch
amount
]
total
compiler
verifier
approver