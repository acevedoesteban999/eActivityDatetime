from odoo import models, fields, api , _

class MailActivity(models.TransientModel):
    _inherit = 'mail.activity.schedule'
    
    is_periodic = fields.Boolean("Is Periodic",default=False,help="The activity will be recreated after it reaches the 'Overdue' state.")
    repetition_period_days = fields.Integer("Repetition Period (Days)",default=1,help="Number of days after which the activity will be created again")
    
    def _action_schedule_activities(self):
        self.ensure_one()
        model = super()._action_schedule_activities()
        model.is_periodic = self.is_periodic
        model.repetition_period_days = self.repetition_period_days
        return model