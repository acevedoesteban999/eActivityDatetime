from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_auto_create_activity = fields.Boolean(
        string='Add Activity on create',
        config_parameter='crm_lead_auto_activity.is_auto_create_activity',
        help="If checked, an activity will be automatically created when a new lead is created.",
    )
    auto_lead_activity_type_id = fields.Many2one(
        comodel_name='mail.activity.type',
        string='Default Activity Type',
        help="Default activity type for the created activity on new lead",
        config_parameter='crm_lead_auto_activity.auto_lead_activity_type_id',
    )
    auto_lead_time_deadline = fields.Float(
        string='Default Activity Deadline',
        help="Default time deadline for the created activity on new lead",
        config_parameter='crm_lead_auto_activity.auto_lead_time_deadline',
    )