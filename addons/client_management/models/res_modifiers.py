# coding=utf-8
from odoo import api, fields, models, _


class IrMenuModifier(models.Model):
    """ Inheriting Ir menu model to allow beneficiary to see only assigned menus. """
    _inherit = 'ir.ui.menu'

    @api.multi
    @api.returns('self')
    def _filter_visible_menus(self):
        menus = super(IrMenuModifier, self)._filter_visible_menus()
        # b_group = self.env.ref('client_management.group_branch_beneficiary')
        # if self.env.user.has_group('client_management.group_branch_beneficiary'):
        #     menus = menus.filtered(lambda menu: menu.parent_id or (not menu.parent_id and b_group.id in menu.groups_id.ids))
        return menus
