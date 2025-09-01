# -*- coding: utf-8 -*-
{
    'name': 'HR Resume',
    'version': '18.0.1.0.0',
    'category': 'Human Resources',
    'summary': """ """,
    'author': 'Arash Homayounfar',
    'company': 'Giladoo',
    'maintainer': 'Giladoo',
    'website': "https://www.giladoo.com",
    'installable': True,
    'auto_install': False,
    'application': False,
    'depends': ['base', 'hr', 'sd_hr', 'sd_projects', 'sd_hr_documents', 'hr_extend'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/sd_hr_documents.xml',
        'views/hr_employee_views.xml',
        'report/resume_en.xml',
        'report/resume_en_template.xml',
    ],
'assets': {
        'web.assets_backend':[
            # 'sd_hr_resume/static/src/components/**/*'
        ],

    },
    'demo': [

    ],
    'images': ['static/description/banner.jpg'],
    'license': 'LGPL-3',
}
