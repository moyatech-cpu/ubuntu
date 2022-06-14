# coding=utf-8
import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from lxml import etree
from odoo.http import request

from odoo.tools.misc import ustr


class TicketDashboard(models.Model):
    """Ticket Dashboard Model."""
    _name = "ticket.dashboard"
    _rec_name = "name"
    _description = "Ticket Dashboard"

    name = fields.Char(string="Title")

    @api.model
    def get_data(self):
        get_lusers_ticket = self.env['helpdesk_lite.ticket'].sudo().search([('user_id', '=', self.env.user.id)])
        get_lusers_hp_ticket = self.env['helpdesk_lite.ticket'].sudo().search(
            [('user_id', '=', self.env.user.id), ('priority', '=', '2')])
        get_lusers_urgent_ticket = self.env['helpdesk_lite.ticket'].sudo().search(
            [('user_id', '=', self.env.user.id), ('priority', '=', '3')])
        get_lusers_normal_ticket = self.env['helpdesk_lite.ticket'].sudo().search(
            [('user_id', '=', self.env.user.id), ('priority', '=', '1')])
        sla_failed_tickets = self.env['helpdesk_lite.ticket'].sudo().search(
            [('user_id', '=', self.env.user.id), ('is_mailed_sla', '=', True)])
        sla_hp_failed_tickets = self.env['helpdesk_lite.ticket'].sudo().search(
            [('user_id', '=', self.env.user.id), ('is_mailed_sla', '=', True), ('priority', '=', '2')])
        sla_urgent_failed_tickets = self.env['helpdesk_lite.ticket'].sudo().search(
            [('user_id', '=', self.env.user.id), ('is_mailed_sla', '=', True), ('priority', '=', '3')])
        sla_normal_failed_tickets = self.env['helpdesk_lite.ticket'].sudo().search(
            [('user_id', '=', self.env.user.id), ('is_mailed_sla', '=', True), ('priority', '=', '1')])
        # new_tickets = self.env['helpdesk_lite.ticket'].sudo().search(
        #     [('stage_id', '=', self.env.ref('helpdesk_lite.stage_new').id)])
        # in_progress_tickets = self.env['helpdesk_lite.ticket'].sudo().search(
        #     [('stage_id', '=', self.env.ref('helpdesk_lite.stage_inprogress').id)])
        # solved_tickets = self.env['helpdesk_lite.ticket'].sudo().search(
        #     [('stage_id', '=', self.env.ref('helpdesk_lite.stage_solved').id)])
        # cancelled_tickets = self.env['helpdesk_lite.ticket'].sudo().search(
        #     [('stage_id', '=', self.env.ref('helpdesk_lite.stage_canceled').id)])
        helpdesk_category_id = self.env['helpdesk.category'].sudo().search([])
        category_wise_tickets_list = []
        for categories in helpdesk_category_id:
            category_dict = {}
            unassigned_tickets = 0
            high_priority_ticekts = 0
            urgent_tickets = 0
            tickets = self.env['helpdesk_lite.ticket'].sudo().search(
                [('helpdesk_category_id', '=', categories.id)])
            for ticket_data in tickets:
                if not ticket_data.user_id:
                    unassigned_tickets += 1
                if ticket_data.priority == '2':
                    high_priority_ticekts += 1
                if ticket_data.priority == '3':
                    urgent_tickets += 1
            category_dict = {
                'name': categories.name,
                'unassigned_tickets': unassigned_tickets,
                'high_priority_ticekts': high_priority_ticekts,
                'urgent_tickets': urgent_tickets,
                'categ_id': categories.id
            }
            category_wise_tickets_list.append(category_dict)
        stage_id = self.env['helpdesk_lite.stage'].sudo().search([])
        stages_list = []
        for stage in stage_id:
            stage_dict = {}
            tickets = self.env['helpdesk_lite.ticket'].sudo().search(
                [('stage_id', '=', stage.id)])
            stage_dict = {
                'name': stage.name,
                'total_tickets': len(tickets),
                'image': stage.dashboard_icon,
                'id': stage.id
            }
            stages_list.append(stage_dict)
        data = {
            'total_tickets': len(get_lusers_ticket),
            'total_hpt': len(get_lusers_hp_ticket),
            'total_ut': len(get_lusers_urgent_ticket),
            'total_nt': len(get_lusers_normal_ticket),
            'failed_sla_total_tickets': len(sla_failed_tickets),
            'failed_sla_total_hpt': len(sla_hp_failed_tickets),
            'failed_sla_total_ut': len(sla_urgent_failed_tickets),
            'failed_sla_total_nt': len(sla_normal_failed_tickets),
            # 'newt': len(new_tickets),
            # 'progresst': len(in_progress_tickets),
            # 'solvedt': len(solved_tickets),
            # 'cancelledt': len(cancelled_tickets),
            'categories': category_wise_tickets_list,
            'stages': stages_list,
            'uid': self.env.user.id,
            # 'new_stage_id': self.env.ref('helpdesk_lite.stage_new').id,
            # 'progress_stage_id': self.env.ref('helpdesk_lite.stage_inprogress').id,
            # 'solved_ticket_id': self.env.ref('helpdesk_lite.stage_solved').id,
            # 'cancelled_ticket_id': self.env.ref('helpdesk_lite.stage_canceled').id,
        }
        return data
