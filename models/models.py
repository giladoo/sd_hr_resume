# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SdHrResumeRecords(models.Model):
    _name = 'sd_hr_resume.records'
    _description = 'sd_hr_resume records'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    employee_id = fields.Many2one('hr.employee')
    job_title = fields.Char(related='employee_id.job_title')
    department_id = fields.Many2one(related='employee_id.department_id')
    project = fields.Many2one(related='employee_id.project')
    education = fields.Text(translate=True)
    experience = fields.Text(translate=True)
    projects = fields.Text(translate=True)
    capabilities = fields.Text(translate=True)
    qualifications = fields.Text(translate=True)
    software = fields.Text(translate=True)
    trainings = fields.Text(translate=True)
    awards = fields.Text(translate=True)

    document_ids = fields.One2many(related='employee_id.document_ids',  domain="[('id', '=', False)]")

