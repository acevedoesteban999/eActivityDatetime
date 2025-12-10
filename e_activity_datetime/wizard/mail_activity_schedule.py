from odoo import models, fields, api , _

class MailActivity(models.TransientModel):
    _inherit = 'mail.activity.schedule'
    
    datetime_deadline = fields.Datetime(
        'Due Date Time', compute="_compute_date_deadline",
        readonly=False, store=True)
    
    all_day = fields.Boolean("All Day",default=True)
    
    @api.depends('activity_type_id','all_day')
    def _compute_date_deadline(self):
        for scheduler in self:
            if scheduler.activity_type_id:
                scheduler.datetime_deadline = scheduler.activity_type_id._get_datetime_deadline()
            elif not scheduler.date_deadline:
                scheduler.datetime_deadline = fields.Datetime.now().replace(second=0)
            
            if scheduler.all_day:
                super(MailActivity, scheduler)._compute_date_deadline()
            else:
                scheduler.date_deadline = scheduler.datetime_deadline.date()
    
    def _action_schedule_activities(self):
        if not self.res_model:
            model = self._action_schedule_activities_personal()
        else:
            model = self._get_applied_on_records().activity_schedule(
                activity_type_id=self.activity_type_id.id,
                automated=False,
                summary=self.summary,
                note=self.note,
                user_id=self.activity_user_id.id,
                date_deadline=self.date_deadline,
            )
        model.datetime_deadline = self.datetime_deadline
        model.all_day = self.all_day
        return model