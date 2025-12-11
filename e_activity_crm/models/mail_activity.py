from odoo import models,fields,api

class MailActivity(models.Model):
    _inherit = 'mail.activity'
    
    is_periodic = fields.Boolean("Is Periodic",default=False,help="The activity will be recreated after it reaches the 'Overdue' state.")
    repetition_period_days = fields.Integer("Repetition Period (Days)",default=1,help="Number of days after which the activity will be created again")
    in_crm_stage = fields.Boolean("In CRM Stage",compute="_compute_in_crm_stage",help="Indicates whether this CRM activity is associated with a automated stage.") 
    repeated = fields.Boolean("Repeated",help="It indicates when the activity has already been repeated.")
    def _compute_in_crm_stage(self):
        for rec in self:
            if rec.res_model == 'crm.lead' and rec.res_id:
                lead = self.env['crm.lead'].browse(rec.res_id)
                rec.in_crm_stage =  lead.stage_id.allow_auto_create_activity
            else:
                rec.in_crm_stage = False
                
    def _to_store_defaults(self, target):
        return super()._to_store_defaults(target) + ['repeated']