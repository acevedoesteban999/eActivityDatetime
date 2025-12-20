from odoo import models,fields

class MailActivity(models.Model):
    _inherit = 'mail.activity'
    
    is_rescheduled = fields.Boolean("Is Rescheduled",default=False,help="The activity will be rescheduled when has 'done' until convert to oportunity")
    reschedule_days = fields.Integer("Reschedule Days",default=1,help="Number of days after the activity will be schedule")
    done_reschedule = fields.Boolean("Done Reschedule",readonly=True,default=False,help="Indicates that the rescheduling process has been completed.")
    crm_type = fields.Char("CRM Type",compute="_compute_crm_type",help="") 
    def _compute_crm_type(self):
        for rec in self:
            if rec.res_model == 'crm.lead' and rec.res_id :
                rec.crm_type =  rec.env['crm.lead'].browse(rec.res_id).type
            else:
                rec.crm_type = False

    def action_feedback_schedule_next(self, feedback=False, attachment_ids=None):
        action = super().action_feedback_schedule_next(feedback=feedback, attachment_ids=attachment_ids)
        if self.is_rescheduled:
            self.write({'done_reschedule': True})
            action['context'] = {
                **action.get('context',{}),
                'default_is_rescheduled': True,
                'default_reschedule_days': self.reschedule_days,
            }
        return action
