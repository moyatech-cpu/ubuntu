from odoo import api, fields, models

class WorkPlanSubmitWizard(models.TransientModel):
    _name = 'work.plan.submit.wizard'
    _description = 'Submit Work Plan Wizard'

    work_plan_report = fields.Binary(string="Submit Work Plan Report")
    work_plan_report_name = fields.Char('File Name')
    #product_inline_bcs_approved = fields.Binary(String="Product Inline with Approved BCS Product and Service Guidelines")
    #product_inline_bcs_approved_name = fields.Char('File Name')

    @api.multi
    def submit_work_plan_report(self):
        
        voucher_application = self.env['voucher.application'].browse(self._context.get('active_id'))
        
        if(voucher_application):
            voucher_application.work_plan_report_name   = self.work_plan_report_name
            voucher_application.work_plan_report        = self.work_plan_report
            voucher_application.status                  = 'work_plan_submitted'
            
            attachment = {
                       'name': str(self.work_plan_report_name),
                       'datas': self.work_plan_report,
                       'datas_fname': self.work_plan_report_name,
                       'res_model': voucher_application._name,
                       'type': 'binary'
                       }
            ir_attechment_id = self.env['ir.attachment'].create(attachment)
            approve_mail_wiz_template = self.env.ref('nyda_grant_and_voucher.send_voucher_work_plan_mail_template')
            if approve_mail_wiz_template:
                approve_mail_wiz_template.attachment_ids = [(6, 0, [])]
    
                approve_mail_wiz_template.attachment_ids = [(4, ir_attechment_id.id)]
    
                approve_mail_wiz_template.with_context(user=self.env.user,beneficiary=voucher_application.email).sudo().send_mail(voucher_application.id, force_send=True)
            return True            


