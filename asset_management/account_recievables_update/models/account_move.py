# -*- coding: utf-8 -*-

import time
from collections import OrderedDict
from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.exceptions import RedirectWarning, UserError, ValidationError
from odoo.tools.misc import formatLang
from odoo.tools import float_is_zero, float_compare
from odoo.tools.safe_eval import safe_eval
from odoo.addons import decimal_precision as dp
from lxml import etree

#----------------------------------------------------------
# Entries
#----------------------------------------------------------

class AccountMove(models.Model):
    _inherit = "account.move"
    
    state = fields.Selection([('draft', 'Unposted'), ('submitted', 'Submitted'), ('posted', 'Posted')], string='Status',
      required=True, readonly=True, copy=False, default='draft',
      help='All manually created new journal entries are usually in the status \'Unposted\', '
           'but you can set the option to skip that status on the related journal. '
           'In that case, they will behave as journal entries automatically created by the '
           'system on document validation (invoices, bank statements...) and will be created '
           'in \'Posted\' status.')
    
    
    @api.multi
    def action_proceed(self):
        return self.write({'state': 'submitted'})
    
    @api.multi
    def assert_balanced(self):
        if not self.ids:
            return True
        prec = self.env['decimal.precision'].precision_get('Account')

        self._cr.execute("""\
            SELECT      move_id
            FROM        account_move_line
            WHERE       move_id in %s
            GROUP BY    move_id
            HAVING      abs(sum(debit) - sum(credit)) > %s
            """, (tuple(self.ids), 10 ** (-max(5, prec))))
        if len(self._cr.fetchall()) != 0:
            raise UserError(_("Cannot create unbalanced journal entry."))
        return True
    
    @api.multi
    def reverse_moves(self, date=None, journal_id=None):
        date = date or fields.Date.today()
        reversed_moves = self.env['account.move']
        for ac_move in self:
            reversed_move = ac_move._reverse_move(date=date,
                                                  journal_id=journal_id)
            reversed_moves |= reversed_move
            #unreconcile all lines reversed
            aml = ac_move.line_ids.filtered(lambda x: x.account_id.reconcile or x.account_id.internal_type == 'liquidity')
            aml.remove_move_reconcile()
            #reconcile together the reconciliable (or the liquidity aml) and their newly created counterpart
            for account in list(set([x.account_id for x in aml])):
                to_rec = aml.filtered(lambda y: y.account_id == account)
                to_rec |= reversed_move.line_ids.filtered(lambda y: y.account_id == account)
                #reconciliation will be full, so speed up the computation by using skip_full_reconcile_check in the context
                to_rec.with_context(skip_full_reconcile_check=True).reconcile()
                to_rec.force_full_reconcile()
        if reversed_moves:
            #reversed_moves._post_validate()
            #reversed_moves.post()
            return [x.id for x in reversed_moves]
        return []