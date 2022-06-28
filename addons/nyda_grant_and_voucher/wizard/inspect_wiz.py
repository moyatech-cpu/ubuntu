from odoo import api, fields, models

class InspectReport(models.TransientModel):
    _name = 'inspect.wiz'
    _description = 'Inspect Report'

    main_inspect_report = fields.Binary('Inspect Report')
    main_inspect_report_name = fields.Char('File Name')


    @api.multi
    def inspect_report_req(self):
        grant_application = self.env['grant.application'].browse(self._context.get('active_id'))
        grant_application.status = 'inspected'
        grant_application.main_inspect_report_name = self.main_inspect_report_name
        grant_application.main_inspect_report = self.main_inspect_report
        return True


