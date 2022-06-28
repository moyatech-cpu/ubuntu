from odoo import api, fields, models

class ReferToHogac(models.TransientModel):
    _name = 'refer.hogac'
    _description = 'Refer To Hogac'

    minute_from_bgarg = fields.Binary('Minute From BGARC')
    minute_from_bgarg_name = fields.Char('File Name')

    declaration_of_interest_refer = fields.Binary('Declaration Of Interes')
    declaration_of_interest_refer_name = fields.Char('File Name')

    @api.multi
    def set_refer_hogac(self):
        """ Sets state to reject. Add logic if need anything once application is moved to reject state. """
        grant_application = self.env['grant.application'].browse(self._context.get('active_id'))
        grant_application.status = 'hogac_review'
        grant_application.is_hogarg = True
        grant_application.minute_from_bgarg = self.minute_from_bgarg
        grant_application.minute_from_bgarg_name = self.minute_from_bgarg_name
        grant_application.declaration_of_interest_refer = self.declaration_of_interest_refer
        grant_application.declaration_of_interest_refer_name = self.declaration_of_interest_refer_name
#