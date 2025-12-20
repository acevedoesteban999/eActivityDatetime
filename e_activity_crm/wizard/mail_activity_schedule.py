from odoo import models, fields, api , _
from odoo.addons.mail.tools.parser import parse_res_ids

class MailActivity(models.TransientModel):
    _inherit = 'mail.activity.schedule'
    
    is_rescheduled = fields.Boolean("Is Rescheduled",default=False,help="The activity will be rescheduled when has 'done' until convert to oportunity")
    reschedule_days = fields.Integer("Reschedule Days",default=1,help="Number of days after the activity will be schedule")
    crm_type = fields.Char("CRM Type",compute="_compute_crm_type",help="") 
    
    def _compute_crm_type(self):
        for rec in self:
            if rec.res_model == 'crm.lead' and rec.res_ids:
                res_ids  = parse_res_ids(rec.res_ids,rec.env)
                res_id =  res_ids and  res_ids[0]
                rec.crm_type =  rec.env['crm.lead'].browse(res_id).type
            else:
                rec.crm_type = False
                
    def _action_schedule_activities(self):
        self.ensure_one()
        model = super()._action_schedule_activities()
        model.is_rescheduled = self.is_rescheduled
        model.reschedule_days = self.reschedule_days
        return model