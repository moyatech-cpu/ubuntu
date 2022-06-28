from odoo import api, fields, models

class DeligenceReport(models.TransientModel):
    _name = 'deligence.wiz'
    _description = 'Due Deligence Report'

    inspection_report = fields.Binary('Inspection Report')
    inspection_report_name = fields.Char('File Name')
    financial_assessment = fields.Binary('Financial Assessment')
    financial_assessment_name = fields.Char('File Name')
    business_plan = fields.Binary('Business Plan')
    business_plan_name = fields.Char('File Name')


    @api.multi
    def deligence_report_req(self):
        grant_application = self.env['grant.application'].browse(self._context.get('active_id'))
        grant_application.status = 'deligence_done'
        deligence_rr = grant_application.write({
            'inspection_report_name': self.inspection_report_name,
            'inspection_report': self.inspection_report,
            'financial_assessment_name': self.financial_assessment_name,
            'financial_assessment': self.financial_assessment,
            'business_plan_name': self.business_plan_name,
            'business_plan': self.business_plan,

        })

        return True
