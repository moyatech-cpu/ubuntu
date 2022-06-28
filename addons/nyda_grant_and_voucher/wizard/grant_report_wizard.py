from odoo import models, fields, api, _
from datetime import date, datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import UserError


class GrantReportWizard(models.TransientModel):
    _name = 'grant.report.wizard'
    _description = 'Grant Report Wizard'

    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    branch_id       = fields.Many2one('res.branch', string="Branch")
    all_branch      = fields.Boolean(string="All Branch", default=True)
    #report_type     = fields.Selection([('num_voucher', 'Number Of Voucher'), ('voucher_values', 'Voucher Values'), ('voucher_all', 'Consolidated')], string="Show")
    report_type     = fields.Selection([('num_voucher', 'Number of Grants'), ('voucher_values', 'Grants Values')], string="Show")
    type = fields.Selection([('all', 'All'),
                             ('received_applications', 'Received'),
                             ('declined_applications', 'Declined'),
                             ('approved_applications', 'Approved'),
                             ('status_bdo', 'BDO Report'),
                             ('status_gender', 'Gender Report'),
                             ('status_disable', 'Disability Report'),
                             ('status_race', 'Race Report'),
                             ('status_branch', 'Branch Report'),
                             ('status_branch_cons', 'Branch Consolidated Report'),
                             ('status_client', '')
                             ],
                            string="Type")
    
    @api.onchange('branch_id')
    def onchange_branch(self):
        if self.branch_id:
            self.all_branch = False

    @api.onchange('all_branch')
    def onchange_all_branch(self):
        if self.all_branch:
            self.branch_id = False

    @api.multi
    def get_grant_report(self, docids, data=None):
        check_start = datetime.strptime(self.start_date, "%Y-%m-%d")
        new_check_date = check_start.strftime("%Y-%m-%d")
        print('----new_check_date---', new_check_date)

        # print('--check date', check_start, type(check_start))
        check_end = datetime.strptime(self.end_date, "%Y-%m-%d")
        new_check_end = check_end.strftime("%Y-%m-%d")
        print('------\n\n\n', check_end)

        if check_start > check_end:
            raise UserError(_('Start date should not be greater than end date.'))
        return self.env.ref('nyda_grant_and_voucher.action_grant_report').report_action(self)

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

        print('---Type---', self.type)
        
        #Post Go-live
        #grant_approved = self.env['grant.application'].search([('status', '=', self.type)])
        grant_approved = self.env['grant.application'].sudo().search([])
        
        #Pre Go-live
        #grant_approved = self.env['grant.application'].sudo().search([('status', 'in', ['edm_approved', 'completed', 'aftercare', 'Legacy'])])
        
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
            print('----grant_totalgrant_totalgrant_total---', grant_total)
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
                'whites': whites}

# @api.multi
# def grant_report_data(self):
#     check_start = datetime.strptime(self.start_date, "%Y-%m-%d")
#     print('------>>>>>>>>', type(check_start))
#     check_end = datetime.strptime(self.end_date, "%Y-%m-%d")
#     print(':::::------------>>>>>', check_end)
#     new_dict = {}
#     final_list = []
#     new_dict.update({'from': str(check_start.date()), 'to': str(check_end.date())})
#     grant_data = self.env['grant.application'].search([])
#     grant_data_approved = self.env['grant.application'].search([('status', '=', 'edm_approved')])
#     grant_lead = self.env['grant.application']
#     grant_id = []
#     for line in grant_data:
#         check_create_date = datetime.strptime(line.create_date, "%Y-%m-%d %H:%M:%S")
#
#         if (check_create_date.date() > check_start.date() and check_create_date.date() < check_end.date() or
#                 check_create_date.date() == check_start.date() or check_create_date.date() == check_end.date()):
#             grant_id.append(line)
#     count = len(grant_data_approved)
#     total = sum(grant_data_approved.mapped('grant_amount_required'))
#     date_grant_app = []
#     # date_grant_apps = []
#     # date_grant_appss = []
#
#     for lines in grant_data_approved:
#         print('------>>>>>nanananaan>>>>>>>\n\n\n\n\n',lines.name)
#         # temp = lines.name
#         # temp_one = lines.population_group
#         # temp_two = lines.gender
#         # print('------------tempppppp', temp)
#         date_grant_app.append(lines)
#         # date_grant_app.append(temp_one)
#         # date_grant_app.append(temp_two)
#
#     for l_id in grant_id:
#         grant_lead |= l_id
#     new_dict.update({'new_leads': grant_lead,
#                      'edm_app_count': count,
#                      'total_grant': total,
#                      'total_temp': date_grant_app})
#
#     final_list.append(new_dict)
#     return final_list
