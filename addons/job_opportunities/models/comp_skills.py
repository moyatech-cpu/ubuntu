# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ComputerSkills(models.Model):
    _name = 'computer.skills'
    _description = 'Computer Skills'

    qualification = fields.Selection(
        [('excellent', 'Excellent'), ('good', 'Good'), ('satisfactory', 'Satisfactory'), ('basic', 'Basic')],
        string="Qualification")
    ms_word = fields.Selection(
        [('excellent', 'Excellent'), ('good', 'Good'), ('satisfactory', 'Satisfactory'), ('basic', 'Basic')],
        string="MS Word")
    excel = fields.Selection(
        [('excellent', 'Excellent'), ('good', 'Good'), ('satisfactory', 'Satisfactory'), ('basic', 'Basic')],
        string="Excel")
    database_system = fields.Selection(
        [('excellent', 'Excellent'), ('good', 'Good'), ('satisfactory', 'Satisfactory'), ('basic', 'Basic')],
        string="Database System(Oracle,CRM,Access,SAP etc.)")
    graphic_design = fields.Selection(
        [('excellent', 'Excellent'), ('good', 'Good'), ('satisfactory', 'Satisfactory'), ('basic', 'Basic')],
        string="Graphic Design")
    int_mo = fields.Selection(
        [('excellent', 'Excellent'), ('good', 'Good'), ('satisfactory', 'Satisfactory'), ('basic', 'Basic')],
        string="Internet Microsoft Outlook")
    accounts = fields.Selection(
        [('excellent', 'Excellent'), ('good', 'Good'), ('satisfactory', 'Satisfactory'), ('basic', 'Basic')],
        string="Accounts")
    quali_att = fields.Binary(strig="Qualification Attachment")
    quali_att_name = fields.Char(strig="Qualification Attachment Name")
    jobs_database_id = fields.Many2one('jobs.database', string="Jobs Database")
