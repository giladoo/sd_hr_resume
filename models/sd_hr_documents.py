
from odoo import models, fields, api, _

class SdHrResumeSdHrDocuments(models.Model):
    _inherit = "sd_hr_documents.attachments"

    resume_document = fields.Boolean(default=False)