# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class LinkTrainer(models.Model):
    _name = 'link.trainer'
    _rec_name = 'trainer_id'
    _description = 'Link Trainer'

    trainer_id = fields.Many2one('res.users', string="Trainer", domain=lambda self: [
        ("groups_id", "=", self.env.ref("bmt_training.group_trainer").id)])
    coordinator_id = fields.Many2one('res.users', string="Co-ordinator", domain=lambda self: [
        ("groups_id", "=", self.env.ref("client_management.group_coordinator").id)])
    branch_manager_id = fields.Many2one('res.users', string="Branch Manager", domain=lambda self: [
        ("groups_id", "=", self.env.ref("client_management.group_branch_manager").id)])
    head_office_admin_id = fields.Many2one('res.users', string="Head Office Admin", domain=lambda self: [
        ("groups_id", "=", self.env.ref("bmt_training.group_ho_admin").id)])
    head_office_manager_id = fields.Many2one('res.users', string="Head Office Manager", domain=lambda self: [
        ("groups_id", "=", self.env.ref("bmt_training.group_ho_manager").id)])

    @api.constrains('trainer_id')
    @api.one
    def restrict_trainer(self):
        trainer_exists = self.env['link.trainer'].sudo().search(
            [('trainer_id', '=', self.trainer_id.id), ('id', '!=', self.id)])
        print ("\n\n\n", trainer_exists, self, self.id)
        if trainer_exists:
            raise ValidationError(_("Trainer is already linked !!"))
