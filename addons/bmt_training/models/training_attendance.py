# coding=utf-8
from odoo import api, fields, models, _
from datetime import date
from datetime import datetime

class TrainingAttendance(models.Model):
    """ This model might help with capturing signatures of the attendees for training sessions.
        Inherit model and add m2o of particular training to create O2m in training model."""
    _name = 'training.attendance'
    _description = "Model to capture attendance for all type of trainings."

    participant_id = fields.Many2one('youth.enquiry', string="Name")
    surname = fields.Char(string="Surname", related="participant_id.surname")
    id_no = fields.Char(string="ID Number", related="participant_id.id_number")
    dob = fields.Date("Date of birth")
    signature = fields.Binary('To be signed by Benificiary during training')
    signature_done = fields.Boolean(string="Signed(Tick when its signed)")
    sp_training_id = fields.Many2one('sales.pitch.training', string="Sales Pitch Training")
    sp_training_id_2 = fields.Many2one('sales.pitch.training', string="Sales Pitch Training 2")
    sp_training_id_3 = fields.Many2one('sales.pitch.training', string="Sales Pitch Training 3")
    session = fields.Char('Session')
    gender = fields.Selection([('male','Male'), ('female', 'Female')], string="Gender")
    geographic_location = fields.Selection(
        [('urban', 'Urban'), ('peri-urban', 'Peri Urban'), ('rural-area-villages', 'Rural area - Villages'),
         ('rural-area-farms', 'Rural area - Farms'), ('informa-settlement', 'Informa settlement')],
        string="Geographic Location")
    is_disabled = fields.Boolean(string="Is Disabled")
    race = fields.Selection(
        [('african', 'African'), ('asian', 'Asian'), ('coloured', 'Coloured'), ('indian', 'Indian'),
         ('white', 'White')], string="Race")
    physical_address = fields.Text(string="Physical Address")
    contact_number = fields.Char(string="Contact Number")
    state = fields.Selection([('confirm','Confirmed'),('reject','Rejected')], string="Status", copy=False)

    # @api.onchange('signature')
    # def onchange_signature(self):
    #     if self.signature:
    #         self.signature_done = True
    #@api.multi
    #def compute_dob(self):
    #    day = self.id_no[:6]
    #    month = self.id_no[:4]
    #    year = self.id_[:2]
    #    stringDOB = day[:-2]+'-'+month[-2]+'-'+year
    #    print(stringDOB)
    #    date_time_obj=date.strptime(stringDOB, '%d/%m/%y')
    #    self.dob = date_time_obj
        
    @api.onchange('participant_id')
    def onchange_participant_id(self):
        self.gender = self.participant_id.gender
        self.geographic_location = self.participant_id.geographic_location
        self.contact_number = self.participant_id.cell_phone_number
        self.race = self.participant_id.population_group
        self.physical_address = self.participant_id.physical_address
        dayv = self.participant_id.id_number
        try:
            dayv = dayv[:6]
            stringDOB = dayv[0]+dayv[1]+'-'+dayv[2]+dayv[3]+'-'+dayv[4]+dayv[5]
            if stringDOB[0] == '8' or stringDOB[0] == '9':
                stringDOB = '19'+stringDOB
            else:
                stringDOB = '20'+stringDOB
            date_object = datetime.strptime(stringDOB, "%Y-%m-%d")
            self.dob = date_object
        except:
            print("Conversion Escape")
            pass

    @api.multi
    def do_confirm(self):
        """ Confermation Done """
        self.state = 'confirm'
        return

    @api.multi
    def do_reject(self):
        """ Reject Done """
        self.state = 'reject'
        return