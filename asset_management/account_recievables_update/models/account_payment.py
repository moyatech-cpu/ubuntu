# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from email.policy import default

MAP_INVOICE_TYPE_PARTNER_TYPE = {
    'out_invoice': 'customer',
    'out_refund': 'customer',
    'in_invoice': 'supplier',
    'in_refund': 'supplier',
}
# Since invoice amounts are unsigned, this is how we know if money comes in or goes out
MAP_INVOICE_TYPE_PAYMENT_SIGN = {
    'out_invoice': 1,
    'in_refund': -1,
    'in_invoice': -1,
    'out_refund': 1,
}


class account_abstract_payment(models.AbstractModel):
    _inherit = "account.abstract.payment"
    
    payment_method_id = fields.Many2one('account.payment.method', string='Payment Method Type', required=False, oldname="payment_method",
        help="Manual: Get paid by cash, check or any other method outside of Odoo.\n"\
        "Electronic: Get paid automatically through a payment acquirer by requesting a transaction on a card saved by the customer when buying or subscribing online (payment token).\n"\
        "Check: Pay bill by check and print it from Odoo.\n"\
        "Batch Deposit: Encase several customer checks at once by generating a batch deposit to submit to your bank. When encoding the bank statement in Odoo, you are suggested to reconcile the transaction with the batch deposit.To enable batch deposit,module account_batch_deposit must be installed.\n"\
        "SEPA Credit Transfer: Pay bill from a SEPA Credit Transfer file you submit to your bank. To enable sepa credit transfer, module account_sepa must be installed ")
    
    partner_type = fields.Selection([('supplier', 'Vendor'),('customer', 'Customer')], string="Partner Type")
    currency_id = fields.Many2one('res.currency', string='Currency', required=False, default=lambda self: self.env.user.company_id.currency_id)

class account_register_payments(models.TransientModel):
    _inherit = "account.register.payments"
    
    @api.model
    def default_get(self, fields):
        rec = super(account_register_payments, self).default_get(fields)
        active_ids = self._context.get('active_ids')

        # Check for selected invoices ids
        if not active_ids:
            raise UserError(_("Programming error: wizard action executed without active_ids in context."))

        invoices = self.env['account.invoice'].browse(active_ids)

        # Check all invoices are open
        #if any(invoice.state != 'open' for invoice in invoices):
        if any(invoice.state != 'recon' for invoice in invoices):
            raise UserError(_("You can only register payments for open invoices"))
        # Check all invoices have the same currency
        if any(inv.currency_id != invoices[0].currency_id for inv in invoices):
            raise UserError(_("In order to pay multiple invoices at once, they must use the same currency."))

        # Look if we are mixin multiple commercial_partner or customer invoices with vendor bills
        multi = any(inv.commercial_partner_id != invoices[0].commercial_partner_id
            or MAP_INVOICE_TYPE_PARTNER_TYPE[inv.type] != MAP_INVOICE_TYPE_PARTNER_TYPE[invoices[0].type]
            for inv in invoices)

        total_amount = self._compute_payment_amount(invoices)

        rec.update({
            'amount': abs(total_amount),
            'currency_id': invoices[0].currency_id.id,
            'payment_type': total_amount > 0 and 'inbound' or 'outbound',
            'partner_id': False if multi else invoices[0].commercial_partner_id.id,
            'partner_type': False if multi else MAP_INVOICE_TYPE_PARTNER_TYPE[invoices[0].type],
            'communication': ' '.join([ref for ref in invoices.mapped('reference') if ref]),
            'invoice_ids': [(6, 0, invoices.ids)],
            'multi': multi,
        })
        return rec
    

class account_payment(models.Model):
    _ihnerit = "account.payment"
    
    state = fields.Selection([('draft', 'Draft'), 
                              ('submitted', 'Submitted'),
                              ('posted', 'Posted'),
                              ('reconciled', 'Reconciled'), 
                              ('sent', 'Sent'), 
                              ('cancelled', 'Cancelled')], readonly=True, default='draft', copy=False, string="Status")
    
    @api.model
    def create(self, vals):

        amount          = vals.get('amount')
        payment_date    = vals.get('payment_date')
        partner_id      = vals.get('partner_id')
        
        existing_payment = self.env['account.payment'].sudo().search([('payment_date', '=', payment_date),
                                                                      ('partner_id', '=', partner_id),
                                                                      ('amount', '=', amount)
                                                                      ])
        if existing_payment:
            raise UserError(_("Please review transactions. You have an identical transaction captured today."))
        
        #vals['currency_id']         = 1
        vals['payment_method_id']   = 2
        
        pay = super(account_payment, self).create(vals)
        return pay
            
    @api.onchange('partner_id')
    def _onchange_partner_type(self):
        # Set partner_id domain
        if self.partner_id:
            #return {'domain': {'partner_id': [(self.partner_type, '=', True)]}}
            #return {'domain': {'partner_id': [('x_is_donor', '=', True)]}}
            return {'domain': {'payment_method_id': [('payment_type', '=', self.payment_type)]}}
    
    #Stipend duplication prevention measure
    @api.onchange('currency_id')
    def _onchange_payment_amount(self):
        
        #existing_payment = self.env['account.payment'].sudo().search([('amount', '=', self.amount)])
        
        # If matching payment found, present a warning
        #if existing_payment:
        view = self.env.ref('sh_message.sh_message_wizard')
        view_id = view and view.id or False
        context = dict(self._context or {})
        context['message'] = "  Please beware that a transaction with similar details was processed today."
        return{
                'name':'Warning!',
                'type':'ir.actions.act_window',
                'view_type':'form',
                'view_mode':'form',
                'res_model':'sh.message.wizard',
                'views':[(view.id, 'form')],
                'view_id':view.id,
                'target':'new',
                'context':context,
        }
    
    """        
    @api.onchange('payment_type')
    def _onchange_payment_type(self):
        if not self.invoice_ids:
            # Set default partner type for the payment type
            if self.payment_type == 'inbound':
                self.partner_type = 'customer'
            elif self.payment_type == 'outbound':
                #self.partner_type = 'supplier'
                self.partner_type = 'customer'
            else:
                self.partner_type = False
        # Set payment method domain
        res = self._onchange_journal()
        if not res.get('domain', {}):
            res['domain'] = {}
        jrnl_filters = self._compute_journal_domain_and_types()
        journal_types = jrnl_filters['journal_types']
        journal_types.update(['bank', 'cash'])
        res['domain']['journal_id'] = jrnl_filters['domain'] + [('type', 'in', list(journal_types))]
        return res
    """
    
    @api.multi
    def unlink(self):
        if any(bool(rec.move_line_ids) for rec in self):
            raise UserError(_("You can not delete a payment that is already posted"))
        if any(rec.move_name for rec in self):
            raise UserError(_('It is not allowed to delete a payment that already created a journal entry since it would create a gap in the numbering. You should create the journal entry again and cancel it thanks to a regular revert.'))
        return super(account_payment, self).unlink()
    
    @api.multi
    def post(self):
        """ Create the journal items for the payment and update the payment's state to 'posted'.
            A journal entry is created containing an item in the source liquidity account (selected journal's default_debit or default_credit)
            and another in the destination reconciliable account (see _compute_destination_account_id).
            If invoice_ids is not empty, there will be one reconciliable move line per invoice to reconcile with.
            If the payment is a transfer, a second journal entry is created in the destination journal to receive money from the transfer account.
        """
        for rec in self:

            if rec.state not in ('draft','submitted','reconciled'):
                raise UserError(_("Only a draft payment can be posted."))

            #if any(inv.state != 'open' for inv in rec.invoice_ids):
            #if any(inv.state != 'post' for inv in rec.invoice_ids):
            #    raise ValidationError(_("The payment cannot be processed because the invoice is not reconciled!"))

            # Use the right sequence to set the name
            if rec.payment_type == 'transfer':
                sequence_code = 'account.payment.transfer'
            else:
                if rec.partner_type == 'customer':
                    if rec.payment_type == 'inbound':
                        sequence_code = 'account.payment.customer.invoice'
                    if rec.payment_type == 'outbound':
                        sequence_code = 'account.payment.customer.refund'
                if rec.partner_type == 'supplier':
                    if rec.payment_type == 'inbound':
                        sequence_code = 'account.payment.supplier.refund'
                    if rec.payment_type == 'outbound':
                        sequence_code = 'account.payment.supplier.invoice'
            rec.name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.payment_date).next_by_code(sequence_code)
            if not rec.name and rec.payment_type != 'transfer':
                raise UserError(_("You have to define a sequence for %s in your company.") % (sequence_code,))

            # Create the journal entry
            amount = rec.amount * (rec.payment_type in ('outbound', 'transfer') and 1 or -1)
            move = rec._create_payment_entry(amount)

            # In case of a transfer, the first journal entry created debited the source liquidity account and credited
            # the transfer account. Now we debit the transfer account and credit the destination liquidity account.
            if rec.payment_type == 'transfer':
                transfer_credit_aml = move.line_ids.filtered(lambda r: r.account_id == rec.company_id.transfer_account_id)
                transfer_debit_aml = rec._create_transfer_entry(amount)
                (transfer_credit_aml + transfer_debit_aml).reconcile()

            rec.write({'state': 'posted', 'move_name': move.name})
        return True
    
    @api.multi
    def action_proceed(self):
        return self.write({'state': 'submitted'})

    @api.multi
    def action_recon(self):
        return self.write({'state': 'reconciled'})
        
    def action_validate_invoice_payment(self):
        """ Posts a payment used to pay an invoice. This function only posts the
        payment by default but can be overridden to apply specific post or pre-processing.
        It is called by the "validate" button of the popup window
        triggered on invoice form by the "Register Payment" button.
        """
        if any(len(record.invoice_ids) != 1 for record in self):
            # For multiple invoices, there is account.register.payments wizard
            raise UserError(_("This method should only be called to process a single invoice's payment."))

        #Process payment
        self.post()
        
        # Update invoice status to paid
        for record in self:
            record.invoice_ids.write({'state': 'paid'})

        view = self.env.ref('sh_message.sh_message_wizard')
        view_id = view and view.id or False
        context = dict(self._context or {})
        context['message'] = "  Invoice has been successfully posted."
        return{
                'name':'Success',
                'type':'ir.actions.act_window',
                'view_type':'form',
                'view_mode':'form',
                'res_model':'sh.message.wizard',
                'views':[(view.id, 'form')],
                'view_id':view.id,
                'target':'new',
                'context':context,
        }        
    