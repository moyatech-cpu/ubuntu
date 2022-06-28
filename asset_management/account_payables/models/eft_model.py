# coding=utf-8
from datetime import date, datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, \
    DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.safe_eval import safe_eval
from odoo import api, exceptions, fields, models, _
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
from odoo.tools.float_utils import float_compare
import base64

import logging

_logger = logging.getLogger(__name__)
    
class EFTClass(models.Model):
    _name='creditor.eft'
    _rec_name = 'batch_id'
    
    batch_id = fields.Many2one('creditor.authorize')
    chequebook = fields.Many2one('account.journal',related='batch_id.chequebook',string="Bank Account")
    #ref = fields.Char('EFT ref')
    #dates
    cheque_number = fields.Char('Cheque Number',related="batch_id.cheque_number")
    partner_ids = fields.Many2many('res.partner',related='batch_id.partner_ids',string="partners")
    cheque_date = fields.Date('Cheque Date')
    creation_date = fields.Date('Creation Date',default= date.today())
    first_action_date = fields.Date('First Action Date')
    purge_date = fields.Date('Purge Date')
    last_action_date = fields.Date('Last Action Date')
    separate = fields.Boolean('Separate',default=True)
    
    incremental_num = fields.Char('Incremental File')
    file_type = fields.Char('Debit File Type: ',default="CATS (SSVS)")
    eft_file = fields.Binary()
    eft_file_name = fields.Char('EFT File')
    ir_attachment = fields.Many2many('ir.attachment','rel_eft_statements','batch_id','attachment_id',string="EFT Documents")
    
    #for reports
    voucher_number = fields.Char('Voucher')
    doc_number =fields.Char('Doc')
    date = fields.Date('Doc')
    amount =fields.Char('Doc')
    
    def create_eft(self):
        #code to create EFT file
            
        for rec in self:
            for document in rec['batch_id']['statement']:
                _logger.info(document)
                for doc in document['transactions']:
                    _logger.info(doc)
                    rec['doc_number'] = doc['doc_number']
                    rec['date'] = doc['date']
                    rec['amount'] = doc['amount']
                    self.voucher_number = self.env['ir.sequence'].next_by_code('voucher.number.payables')
                    '''pdf = self.env.ref('account_payables.action_general_posting_journal').sudo().render_qweb_pdf([rec['id']])[0]
                    if self.separate:
                        attachment = {'name': rec['doc_number']+'_'+doc['creditor']['name']+'.pdf',    
                                      'datas': base64.encodestring(pdf), 
                                      'datas_fname': rec['doc_number']+'_'+doc['creditor']['name']+'.pdf', 
                                      'res_model': 'creditor.eft', 
                                      'res_id': rec['id']}

                        self.env['ir.attachment'].create(attachment)'''
            partner = ''
            address = ''
            rec['eft_file_name'] = rec['incremental_num']
            for sp in rec['partner_ids']:
                partner = sp['name']
                address = sp['x_physical_address']
            file_text = """SB20201016                                                                                                                                     
            SD0010000000001C6320050004076935792{0}                            000000015076500NYDA                                           
            SC001                              D0000450000061117145000000000000000000000000000000{1}                            
            ST00000000000001001000000000000000000000015076500                                                                                              """
            final_string = file_text.format(address, partner)
            rec['eft_file'] = base64.b64encode(bytes(final_string,'utf-8'))
            
        
        return self.env.ref('account_payables.action_print_eft_journal_report').report_action(self)

    @api.model
    def create(self, values):

        if values:
            values['incremental_num'] = self.env['ir.sequence'].next_by_code('creditor.eft')
            #replace lines with defaul line
            
        record_obj = super(EFTClass, self).create(values)
        return record_obj
    
    
        
                        
    
    
    
    
    
    
    
    
    