from odoo import models, fields, api , _ , exceptions

class MailActivity(models.TransientModel):
    _inherit = 'mail.activity.schedule'
    
    datetime_deadline = fields.Datetime(
        'Due DateTime', compute="_compute_date_deadline",
        readonly=False, store=True)
    
    all_day = fields.Boolean("All Day",default=True)
    datetime_start = fields.Datetime('Start DateTime',readonly=False,store=True,index=True)
    datetime_duration = fields.Float("Datetime Duration",compute="_compute_datetime_duration")
                
    
    @api.depends('datetime_start','datetime_deadline')
    def _compute_datetime_duration(self):
        for rec in self:
            if rec.datetime_deadline and rec.datetime_start:
                rec.datetime_duration = (rec.datetime_deadline - rec.datetime_start).total_seconds() / 3600.0
            else:
                rec.datetime_duration = 0
        
    @api.depends('activity_type_id','all_day')
    def _compute_date_deadline(self):
        for rec in self:
            if rec.activity_type_id:
                rec.datetime_start = rec.datetime_deadline = rec.activity_type_id._get_datetime_deadline()
            elif not rec.date_deadline:
                rec.datetime_start = rec.datetime_deadline = fields.Datetime.now().replace(second=0)
            
            if rec.all_day:
                super(MailActivity, rec)._compute_date_deadline()
            else:
                rec.date_deadline = rec.datetime_deadline.date()
    
    def _action_schedule_activities(self):
        if not self.all_day and self.datetime_start and self.datetime_start > self.datetime_deadline:
            raise exceptions.UserError(_("Datetime start can not be after datetime end"))
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
        model.datetime_start = self.datetime_start
        model.all_day = self.all_day
        return model