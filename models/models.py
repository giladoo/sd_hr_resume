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
    name_cv = fields.Char(related='employee_id.name_cv')
    job_title = fields.Char(related='employee_id.job_title')
    department_id = fields.Many2one(related='employee_id.department_id')
    languages = fields.Text(compute='language_list', )
    language_names = fields.Text(compute='language_list', )
    language_skills = fields.Text(compute='language_list', )
    document_list = fields.Html(compute='language_list', )
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
    @api.depends('employee_id')
    def language_list(self):
        for rec in self:
            langu = ''
            langu_name = ''
            langu_skill = ''
            document_list = ''
            hr_documents = self.env['sd_hr_documents.attachments']
            for skill in rec.employee_id.employee_skill_ids:
                if skill.skill_type_id.name == 'Language':
                    langu += f"{skill.skill_id.name:<20}{skill.skill_level_id.name}\n"
                    langu_name += f"{skill.skill_id.name}\n"
                    langu_skill += f"{skill.skill_level_id.name}\n"


            rec.languages = langu
            rec.language_names = langu_name
            rec.language_skills = langu_skill

            documents = hr_documents.search([('employee_id', '=', rec.employee_id.id), ('resume_document', '=', True)])
            document_list = ''
            for document in documents:
                document_list += f"<div class='h6'>{document.document_type.name}: </div>"
                for att in document.attachments:
                    document_list += (f"<div class='ms-5'>{att.name}</div>")
                document_list += f"<div class='my-2 border'></div>"


            rec.document_list = document_list

    def generate_and_download(self,):
        context = self.env.context
        # print(f"\n generate_and_download\n {context}")
        model_name = context.get('model_name', False)
        active_ids = context.get('active_ids', [])
        variable_no = context.get('variable_no', False)
        output_type = context.get('output_type', 'pdf')
        file_prefix = context.get('file_prefix', 'File')
        file_name = context.get('file_name', 'name')
        attach_docs = context.get('attach_docs', False)
        # print('\n>>>>>>>>>>>\n', model_name, active_ids, variable_no, output_type )
        return self.env['sd_hr.export'].sudo().generate_and_download(model_name, active_ids, variable_no, output_type, file_prefix,  file_name, attach_docs )


