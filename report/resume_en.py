# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api , _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, date, timedelta
import pytz
import jdatetime
from odoo import http


# ########################################################################################
class ReportSdHrResumeEnBw(models.AbstractModel):
    _name = 'report.sd_hr_resume.resume_en_template_bw'
    # _name = 'report.hr_employee.sd_hr_resume_en_report'
    _description = 'HR Resume'

    @api.model
    def _get_report_values(self, docids=None, data=None):
        report = self.env['report.sd_hr_resume.resume_en_template']
        data['report_color'] = 'bw'
        return report.get_report_values(docids, data)

# ########################################################################################
class ReportSdHrResumeEnBwHr(models.AbstractModel):
    _name = 'report.sd_hr_resume.resume_en_template_bw_hr'
    _description = 'HR Resume'

    @api.model
    def _get_report_values(self, docids=None, data=None):
        report = self.env['report.sd_hr_resume.resume_en_template']
        data['report_color'] = 'bw'
        docids = self.env['sd_hr_resume.records'].search([('employee_id', 'in', docids)]).ids
        return report.get_report_values(docids, data)

# ########################################################################################
class ReportSdHrResumeEnHr(models.AbstractModel):
    _name = 'report.sd_hr_resume.resume_en_template_hr'
    _description = 'HR Resume'

    @api.model
    def _get_report_values(self, docids=None, data=None):
        report = self.env['report.sd_hr_resume.resume_en_template']
        docids = self.env['sd_hr_resume.records'].search([('employee_id', 'in', docids)]).ids
        return report.get_report_values(docids, data)

# ########################################################################################
class ReportSdHrResumeEn(models.AbstractModel):
    _name = 'report.sd_hr_resume.resume_en_template'
    # _name = 'report.hr_employee.sd_hr_resume_en_report'
    _description = 'HR Resume'

    # ########################################################################################
    def get_report_values(self, docids=None, data=None):
        return self._get_report_values(docids, data)

    # ########################################################################################
    @api.model
    def _get_report_values(self, docids=None, data=None):
        resumes = self.env['sd_hr_resume.records'].browse(docids)
        employee_ids = list([rec.employee_id.id for rec in resumes])
        docs = self.env['hr.employee'].browse(employee_ids)

        errors = []
        doc_data_list = []
        PAGE_LINES = 25
        context = self.env.context
        time_z = pytz.timezone(context.get('tz'))
        date_time = datetime.now(time_z)
        lang = context.get('lang')
        lang = 'en_US'
        date_time1 = self.date_converter(date_time, lang)

        doc_list = []
        educations = {}
        experiences = {}
        experiences_1 = {}
        experiences_2 = {}
        projects_1 = {}
        projects_2 = {}
        qualifications = {}
        capabilities_1 = {}
        capabilities_2 = {}
        software = {}
        trainings = {}
        awards = {}
        languages = {}
        for doc in docs:
            resume = resumes.search([('employee_id', '=', doc.id)])
            educa = []
            exper = []
            proj = []
            quali = []
            capab = []
            soft = []
            train = []
            awar = []
            langu = []

            educa_count = 0
            exper_count = 0
            proj_count = 0
            quali_count = 0
            capab_count = 0
            soft_count = 0
            train_count = 0
            award_count = 0
            langu_count = 0
            for line in doc.resume_line_ids:
                if line.line_type_id.name == 'Education':
                    educa_count += 1 + len(line.description.split('\n')) if line.description else 0
                    educa.append({'id': doc.id,
                                   'name': line.name,
                                   'description': line.description.split('\n') if line.description else [],
                                   'date_start': self.date_converter(line.date_start, lang)['date'],
                                   'date_end': self.date_converter(line.date_end, lang)['date'] if line.date_end else _('Current'),
                                   })
                elif line.line_type_id.name == 'Experience':
                    exper_count += 1 + len(line.description.split('\n')) if line.description else 0
                    exper.append({'name': line.name,
                                  'description': line.description.split('\n') if line.description else [],
                                  'date_start': self.date_converter(line.date_start, lang)['date'],
                                       'date_end': self.date_converter(line.date_end, lang)['date'] if line.date_end else _('Current'),
                                       })
                elif line.line_type_id.name == 'Projects':
                    proj_count += 1 + len(line.description.split('\n')) if line.description else 0
                    proj.append({'name': line.name,
                                  'description': line.description.split('\n') if line.description else [],
                                  'date_start': self.date_converter(line.date_start, lang)['date'],
                                       'date_end': self.date_converter(line.date_end, lang)['date'] if line.date_end else _('Current'),
                                       })
                elif line.line_type_id.name == 'Qualifications':
                    quali_count += 1 + len(line.description.split('\n')) if line.description else 0
                    quali.append({'name': line.name,
                                  'description': line.description.split('\n') if line.description else [],
                                  'date_start': self.date_converter(line.date_start, lang)['date'],
                                       'date_end': self.date_converter(line.date_end, lang)['date'] if line.date_end else _('Current'),
                                       })

            for skill in doc.employee_skill_ids:
                if skill.skill_type_id.name == 'Language':
                    # langu_count += 1 + len(line.description.split('\n')) if line.description else 0
                    langu.append({  'id': doc.id,
                                    'name': skill.skill_id.name,
                                    'level': skill.skill_level_id.name,
                                    })
                elif skill.skill_type_id.name == 'Capabilities':
                    # capab_count += 1 + len(line.description.split('\n')) if line.description else 0
                    capab.append({  'id': doc.id,
                                    'name': skill.skill_id.name,
                                    'level': skill.skill_level_id.name,
                                    })
                elif skill.skill_type_id.name == 'Software':
                    # soft_count += 1 + len(line.description.split('\n')) if line.description else 0
                    soft.append({  'id': doc.id,
                                    'name': skill.skill_id.name,
                                    'level': skill.skill_level_id.name,
                                    })

            # if doc.resume_education and doc.resume_education.strip() != '':
            #     resume_education = doc.resume_education.split('\n')
            #     for record_name in resume_education:
            #         educa_count += len(record_name) // 60 or 1
            #         educa.append({'id': doc.id,
            #                  'name': record_name,
            #                  'description': '',
            #                  'date_start': '',
            #                  'date_end': '',
            #                  })

            if resume.education and resume.education.strip() != '':
                resume_education = resume.education.split('\n')
                for record_name in resume_education:
                    educa_count += len(record_name) // 60 or 1
                    educa.append({'id': doc.id,
                             'name': record_name,
                             'description': '',
                             'date_start': '',
                             'date_end': '',
                             })

            if resume.experience and resume.experience.strip() != '':
                resume_experience = resume.experience.split('\n')
                for record_name in resume_experience:
                    exper_count += len(record_name) // 60 or 1
                    exper.append({'id': doc.id,
                             'name': record_name,
                             'description': '',
                             'date_start': '',
                             'date_end': '',
                             })
            if resume.projects and resume.projects.strip() != '':
                resume_projects = resume.projects.split('\n')
                for record_name in resume_projects:
                    proj_count += len(record_name) // 80 or 1
                    proj.append({'id': doc.id,
                             'name': record_name,
                             'description': '',
                             'date_start': '',
                             'date_end': '',
                             })
            if resume.capabilities and resume.capabilities.strip() != '':
                resume_capabilities = resume.capabilities.split('\n')
                capab_count += len(resume_capabilities)
                for record_name in resume_capabilities:
                    capab_count += len(record_name) // 80 or 1
                    capab.append({'id': doc.id,
                             'name': record_name,
                             'level': '',
                             })
            if resume.qualifications and resume.qualifications.strip() != '':
                resume_qualifications = resume.qualifications.split('\n')
                quali_count += len(resume_qualifications)
                for record_name in resume_qualifications:
                    quali.append({'id': doc.id,
                             'name': record_name,
                             'description': '',
                             'date_start': '',
                             'date_end': '',
                             })

            if resume.software and resume.software.strip() != '':
                resume_software = resume.software.split('\n')
                soft_count += len(resume_software)
                for record_name in resume_software:
                    soft.append({'id': doc.id,
                             'name': record_name,
                             'level': '',
                             })
            if resume.trainings and resume.trainings.strip() != '':
                resume_trainings = resume.trainings.split('\n')
                train_count += len(resume_trainings)
                for record_name in resume_trainings:
                    train.append({'id': doc.id,
                             'name': record_name,
                             'level': '',
                             })
            if resume.awards and resume.awards.strip() != '':
                resume_awards = resume.awards.split('\n')
                award_count += len(resume_awards)
                for record_name in resume_awards:
                    awar.append({'id': doc.id,
                             'name': record_name,
                             'level': '',
                             })

            educations[doc.id] = educa

            # experiences[doc.id] = exper
            # edu_exp_count = educa_count + exper_count
            if 28 - educa_count <= 0:
                experiences_1[doc.id] = []
                experiences_2[doc.id] = exper
            else:
                experiences_1[doc.id] = exper[0: 28 - educa_count]
                experiences_2[doc.id] = exper[28 - educa_count:]

            projects_1[doc.id] = []
            projects_2[doc.id] = proj
            capabilities_1[doc.id] = []
            capabilities_2[doc.id] = capab

            # edu_exp_count = educa_count + exper_count
            # if 20 - edu_exp_count <= 0:
            #     projects_1[doc.id] = []
            #     projects_2[doc.id] = proj
            # else:
            #     projects_1[doc.id] = proj[0: 20 - edu_exp_count]
            #     projects_2[doc.id] = proj[20 - edu_exp_count:]
            #
            # edu_exp_proj_count = educa_count + exper_count + proj_count
            # if edu_exp_count + 10 - edu_exp_proj_count <= 0:
            #     capabilities_1[doc.id] = []
            #     capabilities_2[doc.id] = capab
            # else:
            #     capabilities_1[doc.id] = capab[0: edu_exp_count + 10 - edu_exp_proj_count]
            #     capabilities_2[doc.id] = capab[edu_exp_count + 10 - edu_exp_proj_count:]
            #
            # print(f'edu_exp_proj_count\n    edu_exp_count: {edu_exp_count} \n    edu_exp_proj_count: {edu_exp_proj_count}')

            qualifications[doc.id] = quali
            software[doc.id] = soft
            trainings[doc.id] = train
            awards[doc.id] = awar
            languages[doc.id] = sorted(langu, key=lambda x: x['name'])
        # print(f"#################\n docs: {docs}")
        return {
            'docs': docs,
            'doc_ids': employee_ids,
            'educations': educations,
            'experiences_1': experiences_1,
            'experiences_2': experiences_2,
            'projects_1': projects_1,
            'projects_2': projects_2,
            'qualifications': qualifications,
            'capabilities_1': capabilities_1,
            'capabilities_2': capabilities_2,
            'software': software,
            'trainings': trainings,
            'awards': awards,
            'languages': languages,
        }



    # ########################################################################################
    def date_converter(self, date_time, lang):
        if lang == 'fa_IR':
            date_time = jdatetime.datetime.fromgregorian(datetime=date_time)
            date_time = {'date': date_time.strftime("%Y/%m/%d"),
                  'time': date_time.strftime("%H:%M:%S")}
        else:
            date_time = {'date': date_time.strftime("%Y/%m/%d"),
                        'time': date_time.strftime("%H:%M:%S")}
        return date_time

    # ########################################################################################
    def _table_record(self, items, start_date, first_day, last_day, record_type=False):
        day = len(list([item for item in items
                        if (not record_type or item.record_type.name == record_type)
                        and item.record_date == start_date]))

        month = len(list([item for item in items
                          if (not record_type or item.record_type.name == record_type)
                          and item.record_date <= start_date
                          and item.record_date >= first_day ]))

        total = len(list([item for item in items if (not record_type or item.record_type.name == record_type)]))
        return day, month, total

    # ########################################################################################
    def _table_record_sum_of_records(self, items, start_date, first_day, last_day, record_type=False):
        day = sum(list([item.man_hours for item in items
                        if (not record_type or item.record_type.name == record_type)
                        and item.record_date == start_date]))

        month = sum(list([item.man_hours for item in items
                          if (not record_type or item.record_type.name == record_type)
                          and item.record_date <= start_date
                          and item.record_date >= first_day ]))

        total = sum(list([item.man_hours for item in items if (not record_type or item.record_type.name == record_type)]))
        day = int(round(day, 0))
        month = int(round(month, 0))
        total = int(round(total, 0))
        return day, month, total