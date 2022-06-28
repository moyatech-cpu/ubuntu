from odoo import api, fields, models

class IctCheck(models.TransientModel):
    _name = 'ict.wiz'
    _description = 'ITC Report'

    ict_report = fields.Binary('ITC Report')
    ict_report_name = fields.Char('File Name')

    @api.multi
    def ict_report_req(self):
        grant_application = self.env['grant.application'].browse(self._context.get('active_id'))
        grant_application.status = 'ict_checked'
        grant_application.ict_report_name = self.ict_report_name
        grant_application.ict_report = self.ict_report
        return True

class IctCheck(models.TransientModel):
    _name = 'aftercare.wiz'
    _description = 'Aftercare Report'

    aftercare_report = fields.Binary('Aftercare Report')
    aftercare_report_name = fields.Char('File Name')

    @api.multi
    def aftercare_report_req(self):
        grant_application = self.env['grant.application'].browse(self._context.get('active_id'))
        grant_application.status = 'completed'
        grant_application.aftercare_report_name = self.aftercare_report_name
        grant_application.aftercare_report = self.aftercare_report
        return True

