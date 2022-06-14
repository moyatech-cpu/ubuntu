# -*- coding: utf-8 -*-

from odoo import models, fields


class WizReportRejectComment(models.Model):
    _name = 'wiz.report.reject.comment'
    _description = "Wizard Risk Report Reject Comment"

    comment = fields.Text(string="Comment")

    def action_add_comment(self):
        self.ensure_one()
        report_id = self.env['risk.reporting.history'].browse(self._context.get('active_id'))
        template_id = self.env.ref('nyda_risk_management.email_template_risk_report_reject')
        if report_id:
            report_id.write({'reject_comment': self.comment,
                             'reject_user_id': self.env.user.id or False,
                             'state': 'reject'})
            user = report_id.user_id
            import pdb
            pdb.set_trace()
            if template_id and user and user.email:
                body = "Hello " + user.name + ',<br/>'
                body = body + "Your report for <b>" + (report_id.risk_id.name) + "</b> submited on date " + str(report_id.submit_date) + \
                    " was rejected by <b>" + self.env.user.name + "</b>.<br/>"
                body = body + "<b>Reason for Rejection:</b><br/>" + self.comment
                template_id.write({
                    'email_to': user.email,
                    'body_html': body
                })
                template_id.send_mail(self.id, force_send=True, raise_exception=True)
