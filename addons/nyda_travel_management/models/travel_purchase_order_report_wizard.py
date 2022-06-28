from odoo import models, fields, api
from openerp.osv import orm
from odoo import  _
from datetime import date, datetime
from odoo.exceptions import UserError


class TravelPurchaseReport(models.TransientModel):

        _name= "travel.purchase.order.report.wizard"
        _description = "Travel Purchase Order Report Wizard"
        
        state = fields.Selection([('draft', 'RFQ'),('sent', 'RFQ Sent'),('to approve', 'To Approve'),
                                  ('purchase', 'Purchase Order'),('done', 'Locked'),('cancel', 'Cancelled')],
                                  string='PO Status', default='draft')
        
        start_date = fields.Date(string='Start Date')
        end_date = fields.Date(string='End Date')
        
        @api.multi
        def get_travel_po_report(self):
            
            return self.env.ref('nyda_travel_management.action_travel_purchase_order_report').report_action(self)
                                                    
        @api.model
        def get_travel_purchase_order_data(self):
         
            po_data=[]
            
            sdate = datetime.strptime(self.start_date, '%Y-%m-%d')
            edate = datetime.strptime(self.end_date, '%Y-%m-%d')
                
            if not self.state and not self.start_date and not self.end_date:
                    raise UserError(_("Form content is missing, this report cannot be printed."))
            
            
                
            if self.state:
                    purchase_orders = self.env['purchase.order'].sudo().search([('state','=',self.state)])
                    
            else:
                
                purchase_orders = self.env['purchase.order'].sudo().search([])
                
            if purchase_orders:
                
                for purchase_orders_date in purchase_orders:
                    check_date = datetime.strptime(
                        datetime.strftime(datetime.strptime(purchase_orders_date.create_date, '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d'), '%Y-%m-%d')
                    if sdate <= check_date <= edate:
                        temp={
                            'name' : purchase_orders_date.name,
                            'date_order'   : purchase_orders_date.date_order,
                            'po_status'     : purchase_orders_date.state,
                            'vendor_id'     : purchase_orders_date.partner_id,
                            'amount_tax'    : purchase_orders_date.amount_tax,
                            'amount_total'  : purchase_orders_date.amount_total,
                           }
                        po_data.append(temp)
                    
            return{
                        'data': po_data,
                        'state' : self.state,
                        'start_date': self.start_date,
                        'end_date': self.end_date,
                         }