# coding=utf-8

from odoo import api, fields, models, _
from odoo import http
from datetime import date, datetime


class GrantApplication(models.Model):
    """ Model to register all the appications for grant. """
    _inherit = 'grant.application'
    
    x_grant_applications_count = fields.Integer("No of Grant received",compute='_calculate_total_grants',readonly=True,store=False)

    @api.depends('user_id')
    def _calculate_total_grants(self):
        for record in self:
            grant_exists_ids = self.env['grant.application'].sudo().search([('user_id', '=', record['user_id'].id),('status','in',('approved','completed','aftercare'))])
            record['x_grant_applications_count'] = len(grant_exists_ids)
    
    @api.multi
    def calculated_grants(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Grant Application',
            'res_model': 'grant.application',
            'view_type': 'form',
            'view_mode': 'tree',
            'view_id': self.env.ref('nyda_grant_and_voucher.view_grant_application_tree').id,
            #'views': [(self.env.ref('nyda_grant_and_voucher.view_grant_application_tree').id, 'tree'), (self.env.ref('nyda_grant_and_voucher.view_grant_application_form').id, 'form')],
            'domain': [('user_id', '=', self.user_id.id),('status','in',('approved','completed','aftercare'))],
            'target': 'current',
        }


class GrantReportWizard(models.TransientModel):
    _inherit = 'grant.report.wizard'
    _description = 'Grant Report Wizard'
    
    status = fields.Selection(
        [('approved',"Approved"),('new', 'New'), ('ict_checked', 'ITC Checked'), ('inspected', 'Inspected'),
         ('deligence_done', 'Deligence Done')
            , ('investment_memo_upload', 'Investment  Upload'), ('bgarg_review', 'BGARC Review'),
         ('send_letter', 'Send Rejection Letter'), ('hogac_review', 'HOGAC Review'),
         ('approved', 'Approved'), ('sent_approval_letter', 'Send Approval Letter'),
         ('uploaded_approval_letter', 'Contracting'),
         ('bdo_review', 'BDO Review'), ('branch_manager_review', 'Branch Manager Review'),
         ('disbursement', 'Disbursement Pack'),
         ('bcs_approved', 'BCS Approved'), ('qao_approved', 'QAO Approved'), ('edm_approved', 'EDM Approved'),
         ('approval_revoked', 'Approval Revoked'), ('aftercare', 'Aftercare'), ('completed', 'Completed'),
         ('reject', 'Reject'),('Legacy','Legacy')],
        default='approved',
        string="status")
    
    #update threshold
    grant_threshold = fields.Selection([('all','All'),
        ('threshold_1', 'Threshold 1'),
        ('threshold_2', 'Threshold 2'),
        ('threshold_3',
         'Threshold 3'),
        ('threshold_4',
         'Threshold 4')],
        # ('threshold_5', 'Threshold 5 - for agriculture and technology related  projects - maximum threshold is R250,000.00')
        string="Grant Threshold")
    
    
    @api.multi
    def grant_report_data(self):
        check_start = datetime.strptime(self.start_date, "%Y-%m-%d")
        new_check_date = check_start.strftime("%Y-%m-%d")
        print('------>>>>>>>>', type(check_start))
        check_end = datetime.strptime(self.end_date, "%Y-%m-%d")
        new_check_end = check_end.strftime("%Y-%m-%d")
        print(':::::------------>>>>>', check_end)

        data = {}

        cc = []
        pty = []
        coops = []
        other = []
        
        #Post Go-live
        #grant_approved = self.env['grant.application'].search([('status', 'in', ['edm_approved', 'completed', 'aftercare'])])
        
        #Pre Go-live
        #grant_approved = self.env['grant.application'].search([('status', 'in', ['edm_approved', 'completed', 'aftercare', 'Legacy'])])
        #if self.all_branch:
        #    grant_approved = self.env['grant.application'].search([('status', 'in', ['approved','edm_approved', 'completed', 'aftercare', 'Legacy'])])
        #elif self.branch_id:
        #    grant_approved = self.env['grant.application'].search([('branch_id', '=', self.branch_id.id),('status', 'in', ['approved','edm_approved', 'completed', 'aftercare', 'Legacy'])])
        #added code
        if self.status:
            if self.all_branch:
                branch = 'All Branches'
                if self.grant_threshold == 'all':
                    grant_approved = self.env['grant.application'].sudo().search(
                        [('status', '=', self.status)])
                else:
                    grant_approved = self.env['grant.application'].sudo().search(
                        [('status', '=', self.status),('grant_threshold','=',self.grant_threshold)]) 
            else:
                branch = self.branch_id.name
                if self.grant_threshold == 'all':
                    grant_approved = self.env['grant.application'].sudo().search(
                        [('status', '=', self.status),('branch_id', '=', self.branch_id.id)])
                else:
                    grant_approved = self.env['grant.application'].sudo().search(
                        [('status', '=', self.status),('branch_id', '=', self.branch_id.id),('grant_threshold','=',self.grant_threshold)])
        else:
            if self.all_branch:
                branch = 'All Branches'
                if self.grant_threshold == 'all':
                    grant_approved = self.env['grant.application'].sudo().search([])
                else:
                    grant_approved = self.env['grant.application'].sudo().search(
                        [('grant_threshold','=',self.grant_threshold)]) 
            else:
                branch = self.branch_id.name
                if self.grant_threshold == 'all':
                    grant_approved = self.env['grant.application'].sudo().search(
                        [('branch_id', '=', self.branch_id.id)])
                else:
                    grant_approved = self.env['grant.application'].sudo().search(
                        [('branch_id', '=', self.branch_id.id),('grant_threshold','=',self.grant_threshold)])
        
        
        print('-grant_approved---\n\n\n', grant_approved)
        total_amount_reqs = 0
        lengths = 0
        males = 0
        females = 0
        urbans = 0
        rurals = 0
        africans = 0
        indians = 0
        coloureds = 0
        whites = 0
        for grant_total in grant_approved:
            print('----grant_total grant_total grant_total---', grant_total)
            lengths += 1
            africans += 1 if grant_total.population_group == 'african' else 0
            indians += 1 if grant_total.population_group in ['indian', 'asian'] else 0
            coloureds += 1 if grant_total.population_group == 'coloured' else 0
            whites += 1 if grant_total.population_group == 'white' else 0
            urbans += 1 if grant_total.geographical_type in ['urban', 'peri-urban'] else 0
            rurals += 1 if grant_total.geographical_type not in ['urban', 'peri-urban'] else 0
            males += 1 if grant_total.gender == 'male' else 0
            females += 1 if grant_total.gender == 'female' else 0
            total_amount_reqs += grant_total.grant_amount_required
            print('---total_amount_req---', total_amount_reqs)
            print('---grant_total.grant_amount_required---', grant_total.grant_amount_required)
            print('---population_group---', grant_total.population_group)
            print('---urban---', grant_total.geographical_type)

        grant_entity = self.env['legal.entity'].sudo().search([])
        print(">>>>>>>>>>>>", grant_entity)
        for entity in grant_entity:
            if entity.name == 'CC':
                total_amount_req = 0
                length = 0
                male = 0
                female = 0
                urban = 0
                rural = 0
                african = 0
                indian = 0
                coloured = 0
                white = 0
                for ga in grant_approved:
                    if entity.id in ga.grant_legal_entity_ids.ids:
                        length += 1
                        african += 1 if ga.population_group == 'african' else 0
                        indian += 1 if ga.population_group in ['indian', 'asian'] else 0
                        coloured += 1 if ga.population_group == 'coloured' else 0
                        white += 1 if ga.population_group == 'white' else 0
                        urban += 1 if ga.geographical_type in ['urban', 'peri-urban'] else 0
                        rural += 1 if ga.geographical_type not in ['urban', 'peri-urban'] else 0
                        male += 1 if ga.gender == 'male' else 0
                        female += 1 if ga.gender == 'female' else 0
                        total_amount_req += ga.grant_amount_required
                        # len += ga.id
                cc.append({
                    'total_amount_req': total_amount_req,
                    'length': length,
                    'male': male,
                    'female': female,
                    'urban': urban,
                    'rural': rural,
                    'african': african,
                    'indian': indian,
                    'coloured': coloured,
                    'white': white
                })

            if entity.name == 'PTY':
                total_amount_req = 0
                length = 0
                male = 0
                female = 0
                urban = 0
                rural = 0
                african = 0
                indian = 0
                coloured = 0
                white = 0
                for ga in grant_approved:
                    if entity.id in ga.grant_legal_entity_ids.ids:
                        length += 1
                        african += 1 if ga.population_group == 'african' else 0
                        indian += 1 if ga.population_group in ['indian', 'asian'] else 0
                        coloured += 1 if ga.population_group == 'coloured' else 0
                        white += 1 if ga.population_group == 'white' else 0
                        urban += 1 if ga.geographical_type in ['urban', 'peri-urban'] else 0
                        rural += 1 if ga.geographical_type not in ['urban', 'peri-urban'] else 0
                        male += 1 if ga.gender == 'male' else 0
                        female += 1 if ga.gender == 'female' else 0
                        total_amount_req += ga.grant_amount_required
                        # len += ga.id
                pty.append({
                    'total_amount_req': total_amount_req,
                    'length': length,
                    'male': male,
                    'female': female,
                    'urban': urban,
                    'rural': rural,
                    'african': african,
                    'indian': indian,
                    'coloured': coloured,
                    'white': white
                })
            if entity.name == 'Co-ops':

                total_amount_req = 0
                length = 0
                male = 0
                female = 0
                urban = 0
                rural = 0
                african = 0
                indian = 0
                coloured = 0
                white = 0
                for ga in grant_approved:
                    if entity.id in ga.grant_legal_entity_ids.ids:
                        length += 1
                        african += 1 if ga.population_group == 'african' else 0
                        indian += 1 if ga.population_group in ['indian', 'asian'] else 0
                        coloured += 1 if ga.population_group == 'coloured' else 0
                        white += 1 if ga.population_group == 'white' else 0
                        urban += 1 if ga.geographical_type in ['urban', 'peri-urban'] else 0
                        rural += 1 if ga.geographical_type not in ['urban', 'peri-urban'] else 0
                        male += 1 if ga.gender == 'male' else 0
                        female += 1 if ga.gender == 'female' else 0
                        total_amount_req += ga.grant_amount_required
                        # len += ga.id
                coops.append({
                    'total_amount_req': total_amount_req,
                    'length': length,
                    'male': male,
                    'female': female,
                    'urban': urban,
                    'rural': rural,
                    'african': african,
                    'indian': indian,
                    'coloured': coloured,
                    'white': white
                })
            if entity.name == 'Other':

                total_amount_req = 0
                length = 0
                male = 0
                female = 0
                urban = 0
                rural = 0
                african = 0
                indian = 0
                coloured = 0
                white = 0
                for ga in grant_approved:
                    if entity.id in ga.grant_legal_entity_ids.ids:
                        length += 1
                        african += 1 if ga.population_group == 'african' else 0
                        indian += 1 if ga.population_group in ['indian', 'asian'] else 0
                        coloured += 1 if ga.population_group == 'coloured' else 0
                        white += 1 if ga.population_group == 'white' else 0
                        urban += 1 if ga.geographical_type in ['urban', 'peri-urban'] else 0
                        rural += 1 if ga.geographical_type not in ['urban', 'peri-urban'] else 0
                        male += 1 if ga.gender == 'male' else 0
                        female += 1 if ga.gender == 'female' else 0
                        total_amount_req += ga.grant_amount_required
                        # len += ga.id
                    elif not ga.grant_legal_entity_ids.ids:
                        length += 1
                        african += 1 if ga.population_group == 'african' else 0
                        indian += 1 if ga.population_group in ['indian', 'asian'] else 0
                        coloured += 1 if ga.population_group == 'coloured' else 0
                        white += 1 if ga.population_group == 'white' else 0
                        urban += 1 if ga.geographical_type in ['urban', 'peri-urban'] else 0
                        rural += 1 if ga.geographical_type not in ['urban', 'peri-urban'] else 0
                        male += 1 if ga.gender == 'male' else 0
                        female += 1 if ga.gender == 'female' else 0
                        total_amount_req += ga.grant_amount_required
                        
                other.append({
                    'total_amount_req': total_amount_req,
                    'length': length,
                    'male': male,
                    'female': female,
                    'urban': urban,
                    'rural': rural,
                    'african': african,
                    'indian': indian,
                    'coloured': coloured,
                    'white': white
                })

        print('----enetitdffefy--name--\n\n\n',total_amount_req,african, cc, pty, coops, other)
        data['datas'] = {'cc': cc, 'pty': pty, 'coops': coops, 'other': other}
        print('---------\n\n\n\n', data)
        # print('------dirdir dir -\n\n\n\n',{'cc': cc,
        #         'pty': pty,
        #         'coops': coops,
        #         'other': other,
        #         's_date': new_check_date,
        #         'e_date': new_check_end,
        #         'total_amount_req': total_amount_req,
        #         'length': length,
        #         'male': male,
        #         'female': female,
        #         'urban': urban,
        #         'rural': rural,
        #         'african': african,
        #         'indian': indian,
        #         'coloured': coloured,
        #         'white': white})
        grant_threshold = dict(self._fields['grant_threshold'].selection).get(self.grant_threshold)
        status = dict(self._fields['status'].selection).get(self.status)
        return {'cc': cc,
                'pty': pty,
                'coops': coops,
                'other': other,
                's_date': new_check_date,
                'e_date': new_check_end,
                'total_amount_reqs': total_amount_reqs,
                'lengths': lengths,
                'males': males,
                'females': females,
                'urbans': urbans,
                'rurals': rurals,
                'africans': africans,
                'indians': indians,
                'coloureds': coloureds,
                'whites': whites,
                'type': status,
                'branch':branch,
                'threshold': grant_threshold}
