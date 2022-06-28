# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class OpAdmission(models.Model):
    _inherit = 'op.admission'

    id_no = fields.Char(string="ID Number")

class OpAdmissionRegister(models.Model):
    _inherit = 'op.admission.register'

    no_of_application = fields.Integer(string="No. Of Application")
    branch_id = fields.Many2one('res.branch',string="Branch")
    municipality_id = fields.Many2one('res.municipality',string="Municipality")
    trainer_id = fields.Many2one('res.users', string="Trainer", domain=lambda self: [
        ("groups_id", "=", self.env.ref("bmt_training.group_trainer").id)])
    venue_id = fields.Many2one('op.facility', string="Venue")

    def apply_for_training(self):
        for rec in self:
            print ("\n\n\n\n")
            print ("Rec ", rec)
            if rec.state == 'draft':
                current_user_id = self.env['res.partner'].sudo().search(
                    [('id', '=', self.env.user.partner_id.id)])
                op_admission_id = self.env['op.admission'].sudo().search(
                    [('partner_id', '=', current_user_id.id)])
                if not op_admission_id:
                    all_ben_users = self.env.ref('client_management.group_branch_beneficiary').users.ids
                    all_trainers_users = self.env.ref('bmt_training.group_trainer').users.ids
                    if not self.env.user.id in all_ben_users and not self.env.user.id in all_trainers_users:
                        raise UserError(_("Only beneficiaries or trainers can apply to this course !!"))
                    elif self.env.user.id in all_ben_users:
                        youth = self.env['youth.enquiry'].sudo().search([('user_id', '=', self.env.user.id)])
                        # training_participants = self.env['op.admission'].sudo().create({
                        #     'partner_id': current_user_id.id,
                        #     'title': current_user_id.gender,
                        #     'name': current_user_id.geographic_location,
                        #     'middle_name': current_user_id.gender,
                        #     'last_name': current_user_id.population_group,
                        #     'application_number': youth.physical_address,
                        #     'admission_date': youth.cell_phone_number,
                        #     'application_date': rec.id,
                        #     'birth_date': rec.id,
                        #     'course_id': rec.id,
                        #     'batch_id' : rec.id,
                        #     'state': 'draft'
                        # })
                    elif self.env.user.id in all_trainers_users:
                        action = {
                            'type': 'ir.actions.act_window',
                            'view_type': 'form',
                            'view_mode': 'form',
                            'res_model': 'op.admission.register',
                            'target': 'current',
                            'res_id': rec.id,
                            'flags': {'initial_mode': 'edit'},
                            'context': {'form_view_initial_mode': 'edit', 'force_detailed_view': 'true'}
                        }
                        return action
                else:
                    print ("------------------------->>>>>>>>>>>>>>>>>>.", op_admission_id)
                    raise UserError(
                        _("You can only apply to one training at a time !!"))
            else:
                raise UserError(_("You cannot apply for these training as batch is confirmed !!"))

    @api.depends('admission_ids')
    def compute_admissions(self):
        for rec in self:
            rec.no_of_application = len(rec.admission_ids)
