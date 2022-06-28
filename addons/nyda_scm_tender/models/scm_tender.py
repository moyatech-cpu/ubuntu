# coding=utf-8
import logging
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import date, datetime
from lxml import etree

_logger = logging.getLogger(__name__)

class TenderProcurement(models.Model):
    """ Model for SCM Tender processes """
    _inherit    = 'purchase.requisition'
    _name       = 'nyda.scm.tender'
    _rec_name   = 'tender_number'
    
    @api.multi
    def default_employee_id(self):
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
        if employee:
            return employee.id

    @api.multi
    def default_division(self):
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
        if employee:
            return employee.department_id.id     

    @api.multi
    def default_work_phone(self):
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
        if employee:
            return employee.work_phone
    
    tender_title                = fields.Char("Title", required=True)
    
    state                       = fields.Selection([('prepare_documents', 'Prepare Documents'),
                                                    ('internal_review', 'Internal Review'), 
                                                    ('scm_review', 'SCM Review'),
                                                    ('bsc', 'BSC'),
                                                    ('bac', 'BAC'),
                                                    ('advertising', 'Advertising'),
                                                    ('submit_offers', 'Submit Offers'),
                                                    ('open_record_offers', 'Open and Record Offers'),
                                                    
                                                    ('compliance', 'Compliance eligibility'),
                                                    ('functionality', 'Functionality evaluation'),
                                                    ('calculate_points', 'Calculate points'),
                                                    ('recommend_bidders', 'Recommendation'),
                                                    ('evaluation_report', 'Evaluation report'),
                                                    ('signoff_report', 'Signoff report'),
                                                    ('bac_recommendation', 'BAC'),
                                                    ('ceo_approval', 'CEO Approval'),
                                                    
                                                    ('notify_bidders', 'Notify Bidders'),
                                                    ('formally_accepted_offer', 'Accepted contract offer'),
                                                    ('legal_contracting', 'Legal Contracting'),
                                                    ('capture_contract_award', 'Capture contract award'),
                                                    ('completed', 'Completed'),
                                                    ('rejected', 'Rejected'),
                                                    ('cancelled', 'Cancelled')],string='Status', default='prepare_documents')
    
    name                            = fields.Char("Name", required=True, translate=True, default='')
    description                     = fields.Text(string='Description')
    employee                        = fields.Many2one('hr.employee', string="Requester", related_sudo=False, default=lambda self: self.default_employee_id())
    contact_no                      = fields.Char("Contact No", default=lambda self: self.default_work_phone())
    division_id                     = fields.Many2one('hr.department', string="Division", related_sudo=False, default=lambda self: self.default_division())
    request_date                    = fields.Datetime(string='Request Date', default=fields.Datetime.now)
    delivery_address                = fields.Text(string='Delivery Address')
    evaluation_minimum_score        = fields.Float(string='Minimum Score')
    tender_number                   = fields.Char("Tender Number")
    tender_submission_register      = fields.One2many('scm.tender.submission.register','tender_id',string='Tender Submission Register')
    tender_submission_functional    = fields.One2many('scm.tender.submission.register','tender_id',string='Functional Evaluation', domain=[('compliance_eligibility','=',True)])
    tender_submission_bbbee         = fields.One2many('scm.tender.submission.register','tender_id',string='BBBEE', domain=[('compliance_eligibility','=',True)])
    recommendation                  = fields.Text(string='Recommendation')
    bac_comments                    = fields.Text(string='BAC Comments')
    ceo_comments                    = fields.Text(string='CEO Comments')
    cancel_reason                   = fields.Text(string='Cancel Reason')
    reject_reason                   = fields.Text(string='Reject Reason')
    preference_point_system         = fields.Selection([('80', '80/20'), ('90', '90/10')], string="Preference Points")
    validity_period                 = fields.Selection([('90', '90 days'),('180', '180 days'),('210', '210 days')], string="Validity Period")    
    closing_date_time               = fields.Datetime(string='Closing Date')
    executive_review                = fields.Text(string='Executive Review')
    scm_review                      = fields.Text(string='SCM Review')
    bsc_review                      = fields.Text(string='BSC Review')
    bac_review                      = fields.Text(string='BAC Review')
    closing_date                    = fields.Datetime(string='Closing Date')
    
    end_user_representative         = fields.Many2one('hr.employee', string="End User")
    end_user_signature              = fields.Binary("End User Signature")
    scm_representative              = fields.Many2one('hr.employee', string="SCM Representative")
    scm_representative_signature    = fields.Binary("SCM Signature")
    risk_representative             = fields.Many2one('hr.employee', string="Risk Representative")
    risk_representative_signature   = fields.Binary("Risk Signature")
    no_bids_received                = fields.Integer(string="No. Submissions", compute='_count_tender_submissions')
    
    color                           = fields.Integer(string='Color Index', default=4)
    active                          = fields.Boolean(default=True)    
    
    @api.onchange('state')
    def onchange_state(self):
        if self.state == 'new':
            self.color = 10
        if self.state == 'check_compliance':
            self.color = 1
        if self.state == 'recommendation':
            self.color = 4
        if self.state == 'finished':
            self.color = 3
                
    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]    
    
    @api.depends('tender_submission_register')
    def _count_tender_submissions(self):
        submissions_no = self.env['scm.tender.submission.register'].search_count([('tender_id', '=', self.id)])
        for record in self:
            record.no_bids_received = submissions_no
        
    @api.model
    def create(self, values):
        """ Initially, injecting sequence to application that will be unique for all applications. """
        if values:
            values['tender_number'] = self.env['ir.sequence'].next_by_code('scm.tender.code')
        rec_obj = super(TenderProcurement, self).create(values)
       
        return rec_obj   
    
    @api.multi
    def import_csv(self):
        # this will get executed when you click the import button in your form
        return {}

    # Prepare Tender Phase                                                        
    def prepare_documents(self):
        res = self.write({'state': 'internal_review'})    
        return res

    def internal_review_approve(self):
        res = self.write({'state': 'scm_review'})    
        return res
    
    def internal_review_reject(self):
        res = self.write({'state': 'prepare_documents'})    
        return res    
    
    def scm_review_approve(self):
        res = self.write({'state': 'bsc'})    
        return res

    def scm_review_reject(self):
        res = self.write({'state': 'prepare_documents'})    
    
    def bsc_approve(self):
        res = self.write({'state': 'bac'})    
        return res

    def bsc_reject(self):
        res = self.write({'state': 'scm_review'})    
        return res
    
    def bac_approve(self):
        res = self.write({'state': 'advertising'})    
        return res

    def bac_reject(self):
        res = self.write({'state': 'scm_review'})    
        return res

    def advertising(self):
        res = self.write({'state': 'submit_offers'})    
        return res
    
    def submit_offers(self):
        res = self.write({'state': 'open_record_offers'})    
        return res
    
    def open_record_offers(self):
        res = self.write({'state': 'compliance'})    
        action = self.env.ref('nyda_scm_tender.evaluate_tender_action_window').read()[0]   
        return action
    
    # Evaluate Tender Phase 
    def evaluate_previous_stage(self):
        res = self.write({'state': 'open_record_offers'})    
        action = self.env.ref('nyda_scm_tender.prepare_tender_action_window').read()[0]   
        return action

    def compliance(self):
        res = self.write({'state': 'functionality'})    
        return res    

    def functionality(self):
        res = self.write({'state': 'calculate_points'})    
        return res

    def calculate_points(self):
        res = self.write({'state': 'recommend_bidders'})    
        return res

    def recommend_bidders(self):
        res = self.write({'state': 'evaluation_report'})    
        return res

    def evaluation_report(self):
        res = self.write({'state': 'signoff_report'})    
        return res

    def signoff_report(self):
        res = self.write({'state': 'bac_recommendation'})    
        return res
    
    def bac_recommendation(self):
        res = self.write({'state': 'ceo_approval'})    
        return res    

    def ceo_approval(self):
        res = self.write({'state': 'notify_bidders'})    
        action = self.env.ref('nyda_scm_tender.award_tender_action_window').read()[0]   
        return action
    
    # Award Tender Phase
    def award_previous_stage(self):
        res = self.write({'state': 'ceo_approval'})    
        action = self.env.ref('nyda_scm_tender.evaluate_tender_action_window').read()[0]   
        return action
     
    def notify_bidders_completed(self):
        res = self.write({'state': 'formally_accepted_offer'})    
        return res
    
    def formally_accepted_offer(self):
        res = self.write({'state': 'legal_contracting'})    
        return res

    def legal_contracting(self):
        res = self.write({'state': 'capture_contract_award'})    
        return res
    
    def capture_contract_award(self):
        res = self.write({'state': 'completed'})    
        return res
            
class TenderSubmissionRegister(models.Model):    
    _name = 'scm.tender.submission.register'
    
    tender_id                   = fields.Many2one('nyda.scm.tender',string='Tender')
    csd_report                  = fields.Many2one('supplier.master',string='CSD Report')
    bidder_name                 = fields.Char(string="Bidder Name")
    csd_number                  = fields.Char(string="CSD Number")
    telephone                   = fields.Char(string="Telephone")
    email_address               = fields.Char(string="Email Address")
    tax_status                  = fields.Char(string="Tax Status")
    compliance_eligibility      = fields.Boolean(string='Compliance Eligibility')        
    functionality_score         = fields.Float(string='Functionality Score')   
    functionality_score_pass    = fields.Boolean(string='Functionality Pass')
    price_total                 = fields.Float(string='Price Total')
    price_score                 = fields.Float(string='Price Score')    
    bee_level                   = fields.Integer(string='BEE Level')
    bee_score                   = fields.Integer(string='BEE Score')        
    total_score                 = fields.Float(string='Total Score')
    
    
    def verify_csd_report(self):
        
        # Remove any existing entry
        record = self.env['supplier.master'].sudo().search([('UniqueRegistrationReferenceNumber','=',self.csd_number)]).unlink()
        
        #1. Create csd object
        new_csd_report = self.env['supplier.master'].sudo().create({'UniqueRegistrationReferenceNumber': self.csd_number})
                    
        #2. Run Search CSD method from new object to fetch details
        new_csd_report.update_records();
        
        #3. Link new CSD object to tender submission
        self.csd_report = new_csd_report.id
        
    def csd_report_view(self):
        return {
            'name': _('CSD Report'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'supplier.master',
            'res_id': self.csd_report.id,
            'type': 'ir.actions.act_window'
        }      

    def pre_evaluation_assessment(self):
        
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
                
        #1. Organise data for processing
        submission_id       = self.id
        submission_bidder   = self.bidder_name
        evaluator           = employee.id
                
        #3. Check if the bidder assessment has already been captured by this user
        existing_assessment = self.env['scm.tender.preevaluation.assessment'].search([('employee', '=', evaluator), ('submission_id', '=', submission_id)])
        
        #4. Only capture new scoring items
        if len(existing_assessment) == 0:
            
            _logger.info('New Pre-Evaluation')
          
            #2. Create case sssessment record for completion
            assessment = self.env['scm.tender.preevaluation.assessment'].create({   'tender_id': self.tender_id.id,
                                                                                    'employee': evaluator,
                                                                                    'submission_id': submission_id
                                                                                })
            
            #3. Fetch the scoring sheet
            scoring_items = self.env['scm.tender.preevaluation.sheet'].search([('tender_id', '=', self.tender_id.id)])
        
            #3. Save each in linking table together with bid submission
            for eval_item in scoring_items:
            
                # Save the evaluation items
                evaluation_sheet = self.env['scm.tender.bidder.preevaluation.sheet'].create({
                    'submission_id': submission_id,
                    'employee': evaluator,
                    'sheet_id': eval_item.id,
                    'assessment_id': assessment.id,
                    'tender_id': self.tender_id.id
                })

            #6. Present completed assessment sheet form for completion
            action =  {
                     'name': 'New Pre-Evaluation Assessment',
                     'view_type': 'form',
                     'view_mode': 'form',
                     'res_model': 'scm.tender.preevaluation.assessment',
                     'type': 'ir.actions.act_window',
                     'nodestroy': True,
                     'view_id': (self.env.ref('nyda_scm_tender.scm_tender_pre_evaluation_assessment_form_view').id),
                     'res_id': assessment.id,
                     'target': 'new',
                     'context': {'form_view_initial_mode': 'edit', 'force_detailed_view': 'true'}
                   }
        else:
            
            #Check if the scoring sheet had already been captured for this submission
            existing_items = self.env['scm.tender.bidder.preevaluation.sheet'].sudo().search([('assessment_id', '=', existing_assessment.id)])
           
            #Only capture new scoring items if none exists for whatever reason
            if len(existing_items) == 0:
              
              #3. Fetch the scoring sheet
              scoring_items = self.env['scm.tender.preevaluation.sheet'].sudo().search([('tender_id', '=', self.tender_id.id)])
            
              #3. Save each in linking table together with bid submission
              for eval_item in scoring_items:
                
                # Save the evaluation items
                evaluation_sheet = self.env['scm.tender.bidder.preevaluation.sheet'].create({
                    'submission_id': submission_id,
                    'employee': evaluator,
                    'sheet_id': eval_item.id,
                    'assessment_id': assessment.id,
                    'tender_id': self.tender_id.id
                  })
            
            #If already done present previously completed assessment sheet form for edit
            action =  {  'name': 'Existing Pre-Evaluation Assessment',
                        'view_type': 'form',
                        'view_mode': 'form',
                        'res_model': 'scm.tender.preevaluation.assessment',
                        'type': 'ir.actions.act_window',
                        'nodestroy': True,
                        'view_id': (self.env.ref('nyda_scm_tender.scm_tender_pre_evaluation_assessment_form_view').id),
                        'res_id': existing_assessment.id,
                        'target': 'new',
                        'context': {'form_view_initial_mode': 'edit', 'force_detailed_view': 'true'}
                    }   
        
        return action
    
    def functionality_evaluation_assessment(self):
        
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
        
        #1. Organise data for processing
        submission_id       = self.id
        submission_bidder   = self.bidder_name
        evaluator           = employee.id
        
        #3. Check if the bidder assessment has already been captured by this user
        existing_assessment = self.env['scm.tender.scoring.assessment'].sudo().search([('employee', '=', evaluator), ('submission_id', '=', submission_id)])
        
        #4. Only capture new scoring items
        if len(existing_assessment) == 0:
            
            #2. Create case sssessment record for completion
            assessment = self.env['scm.tender.scoring.assessment'].create({
                                                                            'submission_id': submission_id,
                                                                            'employee': evaluator,
                                                                            'tender_id': self.tender_id.id
                                                                        })
        
            #3. Fetch the scoring sheet
            scoring_items = self.env['scm.tender.scoring.sheet'].sudo().search([('tender_id', '=', self.tender_id.id)])
        
            #3. Save each in linking table together with submission
            for eval_item in scoring_items:
            
                # Save the evaluation items
                evaluation_sheet = self.env['scm.tender.bidder.scoring.sheet'].create({
                                                                                        'submission_id': submission_id,
                                                                                        'assessment_id': assessment.id,
                                                                                        'tender_id': self.tender_id.id,
                                                                                        'sheet_id': eval_item.id
                                                                                      })
         
                #6. Present completed assessment sheet form for completion
                action =  {
                         'name': 'New Tender Functional Evaluation',
                         'view_type': 'form',
                         'view_mode': 'form',
                         'res_model': 'scm.tender.scoring.assessment',
                         'type': 'ir.actions.act_window',
                         'nodestroy': True,
                         'view_id': (self.env.ref('nyda_scm_tender.scm_tender_scoring_assessment_form_view').id),
                         'res_id': assessment.id,
                         'target': 'new',
                         'context': {'form_view_initial_mode': 'edit', 'force_detailed_view': 'true'}
                       }
     
        else:
        
            #Check if the scoring sheet had already been captured for this submission
            existing_items = self.env['scm.tender.bidder.scoring.sheet'].sudo().search([('assessment_id', '=', existing_assessment.id)])
           
            #Only capture new scoring items if none exists for some reason
            if len(existing_items) == 0:
                
                #remove_items = self.env['scm.tender.bidder.scoring.sheet'].sudo().search([('assessment_id', '=', existing_assessment.id)]).unlink()
                
                #Fetch the scoring sheet
                scoring_items = self.env['scm.tender.scoring.sheet'].sudo().search([('tender_id', '=', self.tender_id.id)])
          
                #Save each in linking table together with submission
                for eval_item in scoring_items:     
                    evaluation_sheet = self.env['scm.tender.bidder.scoring.sheet'].create({
                                                                                            'submission_id': submission_id,
                                                                                            'sheet_id': eval_item.id,
                                                                                            'assessment_id': existing_assessment.id,
                                                                                            'tender_id': self.tender_id.id
                                                                                          })
            
            #If already done present previously completed assessment sheet form for edit
            action =  {
                        'name': ' Existing Tender Functional Evaluation',
                        'view_type': 'form',
                        'view_mode': 'form',
                        'res_model': 'scm.tender.scoring.assessment',
                        'type': 'ir.actions.act_window',
                        'nodestroy': True,
                        'view_id': (self.env.ref('nyda_scm_tender.scm_tender_scoring_assessment_form_view').id),
                        'res_id': existing_assessment.id,
                        'target': 'new',
                        'context': {'form_view_initial_mode': 'edit', 'force_detailed_view': 'true'}
                    }  
        
        return action
    
    
class TenderPreEvaluationSheet(models.Model):    
    _name = 'scm.tender.preevaluation.sheet'
    _rec_name = 'required_item'
    
    tender_id                   = fields.Many2one('nyda.scm.tender',string='Tender')
    required_item               = fields.Char(string="Requirement")
    
class TenderPreEvaluationAssessment(models.Model):    
    _name = 'scm.tender.preevaluation.assessment'
    _rec_name = 'submission_id'

    @api.multi
    def default_employee_id(self):
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
        if employee:
            return employee.id
            
    tender_id               = fields.Many2one('nyda.scm.tender',string='Tender')
    submission_id           = fields.Many2one('scm.tender.submission.register',string='Bid Submission')
    submission_bidder       = fields.Char(string='Bidder',related='submission_id.bidder_name')
    bidder_evaluation_sheet = fields.One2many('scm.tender.bidder.preevaluation.sheet','assessment_id',string='Evaluation Sheet')    
    employee                = fields.Many2one('hr.employee',string='Assessor', default=lambda self: self.default_employee_id())
    comments                = fields.Text(string="Comments")    
    
    @api.multi
    def complete_assessment(self):
                
        #1.Get the Tender Submission to Update
        submission = self.env['scm.tender.submission.register'].sudo().search([('id', '=', self.submission_id.id)])
        
        #2. Check if all pre-evaluation sheet items are in order
        eval_items = self.env['scm.tender.bidder.preevaluation.sheet'].sudo().search([('assessment_id', '=', self.id)])
        
        num_checks    = len(eval_items)
        checks_passed = 0
        
        for eval_item in eval_items:
            if eval_item.item_compliance == True:
                checks_passed += 1

        #3. Update the submission record accordingly    
        if num_checks == checks_passed:
            submission.write({'compliance_eligibility': True})
        else:
            submission.write({'compliance_eligibility': False})

        view = self.env.ref('sh_message.sh_message_wizard')
        view_id = view and view.id or False
        context = dict(self._context or {})
        context['message'] =  "             The compliance eligibility assessment has been successfully completed.             "
        return{
                'name':'Pre-Evaluation Assessment Completed',
                'type':'ir.actions.act_window',
                'view_type':'form',
                'view_mode':'form',
                'res_model':'sh.message.wizard',
                'views':[(view.id, 'form')],
                'view_id':view.id,
                'target':'new',
                'context':context,
        }

class TenderBidderPreEvaluationSheet(models.Model):    
    _name = 'scm.tender.bidder.preevaluation.sheet'
    _rec_name = 'assessment_id'
    
    tender_id              = fields.Many2one('nyda.scm.tender',string='Tender')
    assessment_id          = fields.Many2one('scm.tender.preevaluation.assessment',string='Assessment')
    submission_id          = fields.Many2one('scm.tender.submission.register',string='Bid Submission')
    sheet_id               = fields.Many2one('scm.tender.preevaluation.sheet',string='Requirement')
    item_compliance        = fields.Boolean(string="Compliant")
    
    
class TenderScoringSheet(models.Model):    
    _name = 'scm.tender.scoring.sheet'
    _rec_name = 'scoring_item'
    
    tender_id            = fields.Many2one('nyda.scm.tender',string='Tender')
    assessment_id        = fields.Many2one('scm.tender.scoring.assessment',string='Assessment')
    scoring_item         = fields.Char(string="Scoring Item")
    details              = fields.Text(string="Details")
    scoring_matrix       = fields.Text(string="Scoring Matrix")
    weight               = fields.Integer(string="Weight")
            
class TenderBidderScoringEvaluationSheet(models.Model):    
    _name = 'scm.tender.bidder.scoring.sheet'
    _rec_name = 'assessment_id'
    
    tender_id            = fields.Many2one('nyda.scm.tender',string='Tender')
    assessment_id        = fields.Many2one('scm.tender.scoring.assessment',string='Assessment')
    submission_id        = fields.Many2one('scm.tender.submission.register',string='Bid Submission')
    sheet_id             = fields.Many2one('scm.tender.scoring.sheet',string='Requirement')
    weight               = fields.Integer(string="Weight", related='sheet_id.weight')
    item_score           = fields.Selection([('1', '1'),
                                             ('2', '2'), 
                                             ('3', '3'),
                                             ('4', '4'),
                                             ('5', '5')],string='Score')
    item_total           = fields.Integer(string="Total", store=True)    

    @api.onchange('item_score')
    def _onchange_item_total(self):
        self.item_total = (int(self.item_score) * self.weight)
                            
    
class TenderScoringAssessment(models.Model):    
    _name = 'scm.tender.scoring.assessment'
    _rec_name = 'submission_id'
    
    @api.multi
    def default_employee_id(self):
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
        if employee:
            return employee.id
            
    tender_id                   = fields.Many2one('nyda.scm.tender',string='Tender')
    submission_id               = fields.Many2one('scm.tender.submission.register',string='Bid Submission')
    submission_bidder           = fields.Char(string='Bidder',related='submission_id.bidder_name')
    scoring_evaluation_sheet    = fields.One2many('scm.tender.bidder.scoring.sheet','assessment_id',string='Functional Evaluation Sheet')  
    employee                    = fields.Many2one('hr.employee',string='Assessor', default=lambda self: self.default_employee_id())
    comments                    = fields.Text(string="Comments")  
    total_assessment_score      = fields.Float(string="Total Functionality Score")
    assessment_percentage       = fields.Float(string="Functionality Percentage")
    minimum_score_obtained      = fields.Boolean(string="Minimim Score Obtained")
    
    @api.multi
    def complete_assessment(self):
        """ Update the main submission table status on completion of the assessment """

        #1. Claculate bidder score
        bidder_score = 0
        
        for eval_line in self.scoring_evaluation_sheet:  
            bidder_score += eval_line.item_total

        self.total_assessment_score = bidder_score    

        #2. Check if score passes minimum requirementfor the tender
        tender = self.env['nyda.scm.tender'].sudo().search([('id', '=', self.tender_id.id)])
        
        #3. calculate assessment percentage
        self.assessment_percentage = ((self.total_assessment_score/500)*100)
                
        #4.Get the Tender Submission to Update
        submission = self.env['scm.tender.submission.register'].sudo().search([('id', '=', self.submission_id.id)])
        
        submission.write({'functionality_score': self.assessment_percentage})
        
        for score in tender:
          if self.assessment_percentage >= score.evaluation_minimum_score:
            self.minimum_score_obtained = True
            submission.write({'functionality_score_pass': True})
          else:
            self.minimum_score_obtained = False
            submission.write({'functionality_score_pass': False})    
            
        view = self.env.ref('sh_message.sh_message_wizard')
        view_id = view and view.id or False
        context = dict(self._context or {})
        context['message'] =  "             The functionality evaluation assessment has been successfully completed.             "
        return{
                'name':'Functionality Evaluation Completed',
                'type':'ir.actions.act_window',
                'view_type':'form',
                'view_mode':'form',
                'res_model':'sh.message.wizard',
                'views':[(view.id, 'form')],
                'view_id':view.id,
                'target':'new',
                'context':context,
                }   
