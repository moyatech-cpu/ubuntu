# coding=utf-8
import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

'''    
SAMPLE FIELDS:

branch_admin_id = fields.Many2one('res.users', string="Branch Admin")
is_enabled = fields.Boolean(string="Enabled")
sequence = fields.Integer('Branch ID', default=0)
name = fields.Char('Branch Name')
name = fields.DateTime('Branch Name')
    
'''
class DS_GL_Business_Unit(models.Model):
    """ DS_GL_Business_Unit """
    _name = 'DS_GL_Business_Unit'
    _description = 'DS_GL_Business_Unit'

    MemberId = fields.Char('MemberId')
    Label = fields.Char('Label')
    Description = fields.Char('Description')
    HelpText = fields.Char('HelpText')
    RNodeType = fields.Char('RNodeType')
    SBZ = fields.Char('SBZ')
    Source = fields.Char('Source')
    Synchronized = fields.Char('Synchronized')


class DS_GL_Division(models.Model):
    """ DS_GL_Division """
    _name = 'DS_GL_Division'
    _description = 'DS_GL_Division'

    MemberId = fields.Char('MemberId')
    Label = fields.Char('Label')
    Description = fields.Char('Description')
    HelpText = fields.Char('HelpText')
    RNodeType = fields.Char('RNodeType')
    SBZ = fields.Char('SBZ')
    Source = fields.Char('Source')
    Synchronized = fields.Char('Synchronized')
    
class DS_GL_FullAccount(models.Model):
    """ DS_GL_FullAccount """
    _name = 'DS_GL_FullAccount'
    _description = 'DS_GL_FullAccount'

    MemberId = fields.Char('MemberId')
    Label = fields.Char('Label')
    Description = fields.Char('Description')
    Account_MemberId = fields.Char('Account_MemberId')
    Account = fields.Char('Account')
    Account_type = fields.Char('Account_type')
    Full_Description = fields.Char('Full_Description')
    Entity = fields.Char('Entity')
    RNodeType = fields.Char('RNodeType')
    Source = fields.Char('Source')
    Synchronized = fields.Char('Synchronized')
    GL_Division_MemberId = fields.Char('GL_Division_MemberId')
    GL_Division = fields.Char('GL_Division')
    GL_Business_Unit_MemberId = fields.Char('GL_Business_Unit_MemberId')
    GL_Business_Unit = fields.Char('GL_Business_Unit')
    GL_Products_MemberId = fields.Char('GL_Products_MemberId')
    GL_Products = fields.Char('GL_Products')
    GL_Objective_MemberId = fields.Char('GL_Objective_MemberId')
    GL_Objective = fields.Char('GL_Objective')


class DS_GL_Objective(models.Model):
    """ DS_GL_Objective """
    _name = 'DS_GL_Objective'
    _description = 'DS_GL_Objective'

    MemberId = fields.Char('MemberId')
    Label = fields.Char('Label')
    Description = fields.Char('Description')
    HelpText = fields.Char('HelpText')
    RNodeType = fields.Char('RNodeType')
    SBZ = fields.Char('SBZ')
    Source = fields.Char('Source')
    Synchronized = fields.Char('Synchronized')

class DS_GL_Product(models.Model):
    """ DS_GL_Product """
    _name = 'DS_GL_Product'
    _description = 'DS_GL_Product'

    MemberId = fields.Char('MemberId')
    Label = fields.Char('Label')
    Description = fields.Char('Description')
    HelpText = fields.Char('HelpText')
    RNodeType = fields.Char('RNodeType')
    SBZ = fields.Char('SBZ')
    Source = fields.Char('Source')
    Synchronized = fields.Char('Synchronized')

class DS_Scenario(models.Model):
    """ DS_Scenario """
    _name = 'DS_Scenario'
    _description = 'DS_Scenario'

    MemberId = fields.Char('MemberId')
    Label = fields.Char('Label')
    Description = fields.Char('Description')
    HelpText = fields.Char('HelpText')
    RNodeType = fields.Char('RNodeType')
    SBZ = fields.Char('SBZ')
    Source = fields.Char('Source')
    Synchronized = fields.Char('Synchronized')

class DS_Time(models.Model):
    """ DS_Time """
    _name = 'DS_Time'
    _description = 'DS_Time'

    MemberId = fields.Char('MemberId')
    Label = fields.Char('Label')
    Description = fields.Char('Description')
    HelpText = fields.Char('HelpText')
    RNodeType = fields.Char('RNodeType')
    SBZ = fields.Char('SBZ')
    SendTo_MemberId = fields.Char('SendTo_MemberId')
    SendTo = fields.Char('SendTo')
    Source = fields.Char('Source')
    Synchronized = fields.Char('Synchronized')
    TimeFiscalPeriod_MemberId = fields.Char('TimeFiscalPeriod_MemberId')
    TimeFiscalPeriod = fields.Char('TimeFiscalPeriod')
    TimeFiscalQuarter_MemberId = fields.Char('TimeFiscalQuarter_MemberId')
    TimeFiscalQuarter = fields.Char('TimeFiscalQuarter')
    TimeFiscalSemester_MemberId = fields.Char('TimeFiscalSemester_MemberId')
    TimeFiscalSemester = fields.Char('TimeFiscalSemester')
    TimeFiscalTertial_MemberId = fields.Char('TimeFiscalTertial_MemberId')
    TimeFiscalTertial = fields.Char('TimeFiscalTertial')
    TimeFiscalYear_MemberId = fields.Char('TimeFiscalYear_MemberId')
    TimeFiscalYear = fields.Char('TimeFiscalYear')
    TimeMonth_MemberId = fields.Char('TimeMonth_MemberId')
    TimeMonth = fields.Char('TimeMonth')
    TimeQuarter_MemberId = fields.Char('TimeQuarter_MemberId')
    TimeQuarter = fields.Char('TimeQuarter')
    TimeSemester_MemberId = fields.Char('TimeSemester_MemberId')
    TimeSemester = fields.Char('TimeSemester')
    TimeTertial_MemberId = fields.Char('TimeTertial_MemberId')
    TimeTertial = fields.Char('TimeTertial')
    TimeYear_MemberId = fields.Char('TimeYear_MemberId')
    TimeYear = fields.Char('TimeYear')
    TopNode = fields.Char('TopNode')

class DS_TDS_TimeFiscalQuarter(models.Model):
    """ DS_TDS_TimeFiscalQuarter """
    _name = 'DS_TDS_TimeFiscalQuarter'
    _description = 'DS_TDS_TimeFiscalQuarter'

    MemberId = fields.Char('MemberId')
    Label = fields.Char('Label')
    Description = fields.Char('Description')
    HelpText = fields.Char('HelpText')
    RNodeType = fields.Char('RNodeType')
    SBZ = fields.Char('SBZ')
    Source = fields.Char('Source')
    Synchronized = fields.Char('Synchronized')
    
class DS_TimeFiscalSemester(models.Model):
    """ DS_TimeFiscalSemester """
    _name = 'DS_TimeFiscalSemester'
    _description = 'DS_TimeFiscalSemester'

    MemberId = fields.Char('MemberId')
    Label = fields.Char('Label')
    Description = fields.Char('Description')
    HelpText = fields.Char('HelpText')
    RNodeType = fields.Char('RNodeType')
    SBZ = fields.Char('SBZ')
    Source = fields.Char('Source')
    Synchronized = fields.Char('Synchronized')


class DS_TimeFiscalYear(models.Model):
    """ DS_TimeFiscalYear """
    _name = 'DS_TimeFiscalYear'
    _description = 'DS_TimeFiscalYear'

    MemberId = fields.Char('MemberId')
    Label = fields.Char('Label')
    Description = fields.Char('Description')
    HelpText = fields.Char('HelpText')
    RNodeType = fields.Char('RNodeType')
    SBZ = fields.Char('SBZ')
    Source = fields.Char('Source')
    Synchronized = fields.Char('Synchronized')
    
class DS_TimeMonth(models.Model):
    """ DS_TimeMonth """
    _name = 'DS_TimeMonth'
    _description = 'DS_TimeMonth'

    MemberId = fields.Char('MemberId')
    Label = fields.Char('Label')
    Description = fields.Char('Description')
    HelpText = fields.Char('HelpText')
    RNodeType = fields.Char('RNodeType')
    SBZ = fields.Char('SBZ')
    Source = fields.Char('Source')
    Synchronized = fields.Char('Synchronized')
    
class DS_TimeQuarter(models.Model):
    """ DS_TimeQuarter """
    _name = 'DS_TimeQuarter'
    _description = 'DS_TimeQuarter'

    MemberId = fields.Char('MemberId')
    Label = fields.Char('Label')
    Description = fields.Char('Description')
    HelpText = fields.Char('HelpText')
    RNodeType = fields.Char('RNodeType')
    SBZ = fields.Char('SBZ')
    Source = fields.Char('Source')
    Synchronized = fields.Char('Synchronized')        

class FACT_Financials_default_partition(models.Model):
    """ FACT_Financials_default_partition """
    _name = 'FACT_Financials_default_partition'
    _description = 'FACT_Financials_default_partition'

    Account_MemberId = fields.Char('Account_MemberId')
    BusinessProcess_MemberId = fields.Char('BusinessProcess_MemberId')
    BusinessRule_MemberId = fields.Char('BusinessRule_MemberId')
    Currency_MemberId = fields.Char('Currency_MemberId')
    Entity_MemberId = fields.Char('Entity_MemberId')
    Scenario_MemberId = fields.Char('Scenario_MemberId')
    Time_MemberId = fields.Char('Time_MemberId')
    TimeDataView_MemberId = fields.Char('TimeDataView_MemberId')
    
    Version_MemberId = fields.Char('Version_MemberId')
    GL_Division_MemberId = fields.Char('GL_Division_MemberId')
    GL_Product_MemberId = fields.Char('GL_Product_MemberId')
    ChangeDatetime = fields.Datetime('ChangeDatetime')
    Financials_Value = fields.Char('Financials_Value')
    GL_Business_Unit_MemberId = fields.Char('GL_Business_Unit_MemberId') 
    GL_FullAccount_MemberId = fields.Char('GL_FullAccount_MemberId') 
    GL_Objective_MemberId = fields.Char('GL_Objective_MemberId') 

class HC_Account(models.Model):
    """ HC_Account """
    _name = 'HC_Account'
    _description = 'HC_Account'

    Hierarchy = fields.Char('Hierarchy')
    ParentId = fields.Char('ParentId')
    MemberId = fields.Char('MemberId')
    SequenceNumber = fields.Char('SequenceNumber')

class HC_GL_FullAccount(models.Model):
    """ HC_GL_FullAccount """
    _name = 'HC_GL_FullAccount'
    _description = 'HC_GL_FullAccount'

    Hierarchy = fields.Char('Hierarchy')
    ParentId = fields.Char('ParentId')
    MemberId = fields.Char('MemberId')
    SequenceNumber = fields.Char('SequenceNumber')    

class HC_GL_Objective(models.Model):
    """ HC_GL_FullAccount """
    _name = 'HC_GL_FullAccount'
    _description = 'HC_GL_FullAccount'

    Hierarchy = fields.Char('Hierarchy')
    ParentId = fields.Char('ParentId')
    MemberId = fields.Char('MemberId')
    SequenceNumber = fields.Char('SequenceNumber')
    
class HC_GL_Product(models.Model):
    """ HC_GL_FullAccount """
    _name = 'HC_GL_FullAccount'
    _description = 'HC_GL_FullAccount'

    Hierarchy = fields.Char('Hierarchy')
    ParentId = fields.Char('ParentId')
    MemberId = fields.Char('MemberId')
    SequenceNumber = fields.Char('SequenceNumber')    

class HC_Time(models.Model):
    """ HC_Time """
    _name = 'HC_Time'
    _description = 'HC_Time'

    Hierarchy = fields.Char('Hierarchy')
    ParentId = fields.Char('ParentId')
    MemberId = fields.Char('MemberId')
    SequenceNumber = fields.Char('SequenceNumber')

class HL_Account_Account(models.Model):
    """ HL_Account_Account """
    _name = 'HL_Account_Account'
    _description = 'HL_Account_Account'

    Parent_L1 = fields.Char('Parent_L1')
    Parent_L2 = fields.Char('Parent_L2')
    Parent_L3 = fields.Char('Parent_L3')
    Parent_L4 = fields.Char('Parent_L4')
    Parent_L5 = fields.Char('Parent_L5')
    SequenceNumber = fields.Char('SequenceNumber')

class HL_GL_FullAccount_All_FullAccounts(models.Model):
    """ HL_GL_FullAccount_All_FullAccounts """
    _name = 'HL_GL_FullAccount_All_FullAccounts'
    _description = 'HL_GL_FullAccount_All_FullAccounts'

    Parent_L1 = fields.Char('Parent_L1')
    Parent_L2 = fields.Char('Parent_L2')
    SequenceNumber = fields.Char('SequenceNumber')

class HL_GL_Objective_All_Objectives(models.Model):
    """ HL_GL_Objective_All_Objectives """
    _name = 'HL_GL_Objective_All_Objectives'
    _description = 'HL_GL_Objective_All_Objectives'

    Parent_L1 = fields.Char('Parent_L1')
    Parent_L2 = fields.Char('Parent_L2')
    SequenceNumber = fields.Char('SequenceNumber')

class HL_GL_Product_GL_Product(models.Model):
    """ HL_GL_Product_GL_Product """
    _name = 'HL_GL_Product_GL_Product'
    _description = 'HL_GL_Product_GL_Product'

    Parent_L1 = fields.Char('Parent_L1')
    Parent_L2 = fields.Char('Parent_L2')
    SequenceNumber = fields.Char('SequenceNumber')

class O_DS_Account(models.Model):
    """ O_DS_Account """
    _name = 'O_DS_Account'
    _description = 'O_DS_Account'

    MemberId = fields.Char('MemberId')
    Label = fields.Char('Label')
    Description = fields.Char('Description')
    AccountType = fields.Char('AccountType')
    Sign = fields.Char('Sign')
    TimeBalance = fields.Char('TimeBalance')
    BP_Budget_MemberId = fields.Char('BP_Budget_MemberId')
    BP_Budget = fields.Char('BP_Budget')
    HelpText = fields.Char('HelpText')
    KeyName_Account = fields.Char('KeyName_Account')
    Rate_MemberId = fields.Char('Rate_MemberId')
    Rate = fields.Char('Rate')
    RNodeType = fields.Char('RNodeType')
    SBZ = fields.Char('SBZ')
    Source = fields.Char('Source')
    Synchronized = fields.Char('Synchronized')

class SecurityRoleMembers(models.Model):
    """ SecurityRoleMembers """
    _name = 'SecurityRoleMembers'
    _description = 'SecurityRoleMembers'

    name        = fields.Char('RoleLabel')
    WinUser     = fields.Char('WinUser')
    WinGroup    = fields.Char('WinGroup')






    