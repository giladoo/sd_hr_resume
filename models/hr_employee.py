# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import logging


class SdHrresumeEmployee(models.Model):
    _inherit = 'hr.employee'

    def _get_report_resume_filename(self, model_name):
        self.ensure_one()
        if model_name == 'sd_hr_resume.records':
            resume = self.env[model_name].browse(self.id)
            name = resume.employee_id.name_cv if len(resume) == 1 else ''
        else:
            name = self.name_cv
        return f"IPAC_Resume_[{name}]"

    def update_resume(self):
        active_ids = self.env.context.get('active_ids')
        # print(f"\n active_ids: {active_ids}")
        hr_resume = self.env['sd_hr_resume.records']
        records = self.browse(active_ids)
        for rec in records:
            # print(f"\n >>> resume_extend: {rec.resume_extend}")
            # print(f"\n >>> resume_education: {rec.resume_education}")
            resume = hr_resume.search([('employee_id', '=', rec.id)])
            if len(resume) == 0:
                resume = hr_resume.create({'employee_id': rec.id})
            resume.education = rec.resume_education
            resume.experience = rec.resume_experience
            resume.projects = rec.resume_projects
            resume.capabilities = rec.resume_capabilities
            resume.qualifications = rec.resume_qualifications
            resume.software = rec.resume_software
            resume.trainings = rec.resume_trainings
            resume.awards = rec.resume_awards

    def open_resume_record(self):
        context = self.env.context
        # print(f"\n >>>>>> context: {context} \n {self}")
        res_id = self.env['sd_hr_resume.records'].search([('employee_id', '=', self.id)])
        if len(res_id) == 0:
            res_id = self.env['sd_hr_resume.records'].create({'employee_id': self.id})
        return {
            'type': 'ir.actions.act_window',
            'target': 'new',
            'name': _('Uninstall module'),
            'res_id': res_id.id,
            'view_mode': 'form',
            'res_model': 'sd_hr_resume.records',
            # 'context': {'default_module_id': self.id},
        }

    # document_ids = fields.One2many('sd_hr_resume.attachments',
    #                                'employee_id',
    #                                string="resume")
    #
    #
    # document_count = fields.Integer(compute='_compute_document_count',
    #                                 string='resume',
    #                                 help='Count of resume.')
    #
    # def _compute_document_count(self):
    #     for rec in self:
    #         rec.document_count = len(rec.document_ids)
    #
    #
    # def action_document_view(self):
    #     self.ensure_one()
    #     context = dict(self.env.context)
    #     context['default_employee_id'] = self.id
    #     domain = [('employee_id', '=', self.id)]
    #     # return {}
    #     return {
    #         'name': _('resume'),
    #         'domain': domain,
    #         'res_model': 'sd_hr_resume.attachments',
    #         'type': 'ir.actions.act_window',
    #         'view_id': False,
    #         'view_mode': 'tree,form',
    #         'context': context,
    #     }
    #
    #
    # @api.model_create_multi
    # def create(self, vals_list):
    #     res = super().create(vals_list)
    #     resume = self.create_resume(res.id, False)
    #     if not resume:
    #         logging.error(f"Default resume for new employee failed, res_id: {res.id}")
    #     return res
    #
    # def create_resume(self, employee_id, res_id):
    #     resume_model = self.env['sd_hr_resume.attachments']
    #     auto_create = self.env['sd_hr_resume.document_type'].search([('auto_create', '=', True)])
    #     try:
    #         for rec in auto_create:
    #             resume_model.create({
    #                 'employee_id': employee_id,
    #                 'relative_id': res_id,
    #                 'document_type': rec.id,
    #                 'name': rec.name,
    #             })
    #         done = True
    #     except Exception as e:
    #         done = False
    #
    #     return done