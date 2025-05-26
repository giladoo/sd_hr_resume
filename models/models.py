# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SdHrResumeRecords(models.Model):
    _name = 'sd_hr_resume.records'
    _description = 'sd_hr_resume records'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    # _rec_name = 'job_title'

    employee_id = fields.Many2one('hr.employee')
    name = fields.Char(related='employee_id.name')
    job_title = fields.Char(related='employee_id.job_title')
    department_id = fields.Many2one(related='employee_id.department_id')
    # department_id = fields.Many2one('hr.department', compute='_department_id', store=True)
    project = fields.Many2one(related='employee_id.project')
    work_location_id = fields.Many2one(related='employee_id.work_location_id')
    education = fields.Text(translate=True)
    experience = fields.Text(translate=True)
    projects = fields.Text(translate=True)
    capabilities = fields.Text(translate=True)
    qualifications = fields.Text(translate=True)
    software = fields.Text(translate=True)
    trainings = fields.Text(translate=True)
    awards = fields.Text(translate=True)

    # document_ids = fields.One2many(related='employee_id.document_ids',  domain=[('employee_id', '=', False)])
    # document_ids = fields.One2many('sd_hr_documents.attachments', 'employee_id', )
    # document_ids = fields.Many2many('sd_hr_documents.attachments',  )


    # @api.depends('employee_id')
    # def _department_id(self):
    #     for rec in self:
    #         print(f'==========>>>>>>>>>>>>> {rec.employee_id}')
    #         rec.department_id = rec.employee_id.department_id.id

