# coding=utf-8
import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class PartnerInherit(models.Model):
    """ Inheriting Partner model to add service rating on service provider. """
    _inherit = 'res.partner'

    service_rating = fields.Selection([('0', 'None'),('1', 'Poor'),('2', 'Fair'),('3', 'Average'),('4', 'Good'),('5', 'Excellent')],"Service Rating", compute='_compute_service_rating')

    @api.multi
    def _compute_service_rating(self):
        '''
        _logger.info('1: Calling Calc Method %s', self.id)

        #Get all the vouchers this service provider has been appointed on
        vouchers = self.env['voucher.application'].search([('x_service_provider', '=', self.id)])
        final_rating    = 0
        total_ranking   = 0
        total_vouchers  = 0

        if vouchers:
            for voucher in vouchers:

                _logger.info('2: Voucher Returned %s', voucher)

                total_vouchers += 1

                #Get all the ratings submitted
                ratings = self.env['voucher.assessment'].search([('voucher_application_id', '=', voucher.id)])
                if ratings:
                    _logger.info('3: Ratings %s', ratings)
                    for assessment in ratings:
                        _logger.info('4: Overall Experience%s', assessment.service_rating_assessment_total)
                        total_ranking += int(assessment.service_rating_assessment_total)

        _logger.info('5: Total Ranking %s', total_ranking)
        if total_vouchers:
            final_rating = 5*(total_ranking/(total_vouchers*25))
        else:
            final_rating = 0
        _logger.info('6: Final Rating %s', final_rating)

        if final_rating >= 4:
            self.service_rating = '5' #'Excellent'

        if final_rating >= 3 and final_rating < 4:
            self.service_rating = '4' #'Good'

        if final_rating >= 2 and final_rating < 3:
            self.service_rating = '3' #'Average'

        if final_rating >= 1 and final_rating < 2:
            self.service_rating = '2' #'Fair'

        if final_rating >= 0 and final_rating < 1:
            self.service_rating = '1' #'Poor'
        '''
