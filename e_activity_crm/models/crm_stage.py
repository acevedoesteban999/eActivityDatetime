from odoo import models,fields,api

class CrmStage(models.Model):
    _inherit = 'crm.stage'

    allow_auto_create_activity = fields.Boolean("Allow Auto Create Activity",default=False,help="If checked, an activity will be automatically created when a lead reaches this stage.")