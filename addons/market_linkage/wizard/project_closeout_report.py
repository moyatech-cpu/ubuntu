from odoo import api, fields, models
from odoo.exceptions import UserError

class ProjectCloseout(models.TransientModel):
    _name = 'project.closeout'
    _description = 'Project Report'

    project_closeout_report = fields.Binary('Project Closeout Report')
    file_name = fields.Char('File Name')

    @api.multi
    def project_closeout_report_req(self):
        user = self.env['register.opportunity'].browse(self._context.get('active_id'))
        user.project_closeout_file_name = self.file_name
        user.project_closeout_report = self.project_closeout_report
        if user.project_closeout_file_name :
        	user.state = 'project_closeout'
        else :
        	raise UserError('Please upload a report')	
        return True

