# coding=utf-8
from datetime import date, datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, \
    DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.safe_eval import safe_eval
from odoo import api, exceptions, fields, models, _
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
from odoo.tools.float_utils import float_compare

import logging

_logger = logging.getLogger(__name__)
# mapping invoice type to refund type

class VSPform(models.Model):
    """ Model to populate voucher applications for specific service provider """
    _inherit = 'bcs.vsp'
    
    @api.multi
    def post_invoices(self):
        line_totals = 0
        move_totals = 0
        journals=[]
        #create payable batch
        payable_batch = self.env['payable.batch'].create({
            'date': self.date,
            'batch_id':self.bcs_number,
            'posting_date': self.date,
            'comment': "BCS VOUCHER SERVICE PROVIDER PAYMENTS: BRANCH – SERVICE PROVIDER",
            'total_amount': self.total_vouchers,
            'batch_type':'voucher',
            'vp_link': self.id,
            })
        
        for inv in self.voucher_invoices:
            #inv.action_invoice_open()
            inv.batch_id_payables = payable_batch.id
            '''if inv.move_id:
                inv.move_id.move_total = inv.amount_total_signed
                inv.move_id.batch_id_payables = payable_batch.id
                move_totals+=1
                for line_record in inv.move_id.line_ids:
                    line_totals+=1
                journals.append(inv.move_id.id)'''
        self.fin_status = 'paid'
        '''try:
            payable_batch.post_journal()
        except Exception:
            pass'''
    
    @api.multi
    def generate_invoices(self):
        for rec in self:
            vps = rec['voucher_application_ids']
            for record in vps:
                accounts = self.env['account.account'].sudo().search([('code','=','000-000-000-9100-0000000')])
                account_id = self.env['account.account']
                journal_id = self.env['account.journal']
                for acc in accounts:
                    account_id = acc
                journals = self.env['account.journal'].sudo().search([('name','=','Vendor Invoices')])
                for jn in journals:
                    journal_id = jn
                inv_total = 0.0
                inv_des = ''
                for line in record['x_recommended_service']:
                    inv_total = inv_total + line['voucher_value']
                    inv_des = inv_des+line['name']+' '
                invoice_id = self.env['account.invoice'].create({
                    'name' : record['invoice_number'],
                    'invoice_number_entry': record['invoice_number'],
                    'date_invoice' : date.today(),
                    'sales_amount' :inv_total,
                    'partner_id': record['x_service_provider']['id'],
                    'user_id': self.env.uid,
                    'type':'in_invoice',
                    'account_id':account_id.id,
                    'journal_id':journal_id.id,
                    'related_vp':rec['id'],
                    'state':'draft',
                    
                })
                
                product_ids = self.env['product.product'].sudo().search([('name','=','VOUCHER ITEM')])
                product_id = self.env['product.product']
                if not product_ids:
                    category_id = self.env['product.category'].sudo().search([('name','=','All')])
                    for cat in category_id:
                        product_id = self.env['product.product'].create({
                            'type' : 'service',
                            'name' : 'VOUCHER ITEM',
                            'default_code' : 'VOUCHER ITEM',
                            'categ_id' : cat.id,
                        })
                else:
                    for prod in product_ids:
                        product_id = prod
                prod_accounts = self.env['account.account'].sudo().search([('code','=','1995')])
                self.env['account.invoice.line'].create({
                        'invoice_id' : invoice_id.id,
                        'name' : 'VOUCHER ITEM',
                        'product_id' : product_id.id,
                        'price_unit' : inv_total,
                        'quantity' : 1.0,
                        'account_id': prod_accounts.id,
                    })
                rec['voucher_invoices'] = rec['voucher_invoices'] + invoice_id
            rec['fin_status'] = 'open'