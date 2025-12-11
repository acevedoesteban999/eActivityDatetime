from odoo import models,fields,api
from datetime import datetime,UTC
from odoo.addons.e_activity_datetime.utils.date import get_server_utc_datetime
class MailActivity(models.Model):
    _inherit = 'mail.activity'
    
    datetime_deadline = fields.Datetime('Due Date Time',readonly=False,store=True,compute="_compute_datetime_deadline",index=True,default=fields.Datetime.now().replace(second=0))
    date_deadline = fields.Date('Due Date',store=True,readonly=False,compute="_compute_date_deadline", index=True, required=True, default=fields.Date.context_today)
    all_day = fields.Boolean("All Day",default=True)
    
    @api.depends('datetime_deadline','all_day')
    def _compute_date_deadline(self):
        for rec in self:
            if not rec.all_day and rec.datetime_deadline:
                rec.date_deadline =  rec.datetime_deadline.date()
            else:
                rec.date_deadline = rec.date_deadline or fields.Date.today()

    @api.depends('date_deadline','all_day')
    def _compute_datetime_deadline(self):
        for rec in self:
            if rec.all_day:
                utc_datetime = get_server_utc_datetime(7,0)
                rec.datetime_deadline = utc_datetime
            
            else:
                rec.datetime_deadline = rec.datetime_deadline or fields.Datetime.now().replace(second=0)
                
    def _to_store_defaults(self, target):
        return super()._to_store_defaults(target) + ['datetime_deadline','all_day']
    
    
    @api.depends('active', 'date_deadline','datetime_deadline','all_day')
    def _compute_state(self):
        for record in self.filtered(lambda activity: activity.date_deadline or activity.datetime_deadline):
            tz = record.user_id.sudo().tz
            if not record.active:
                record.state = 'done' 
            elif record.all_day: 
                record.state = record._compute_state_from_date(record.date_deadline, tz)
            else:
                record.state = record._compute_state_from_datetime(record.datetime_deadline, tz)

    @api.model
    def _compute_state_from_datetime(self, datetime_deadline, tz=False):
        datetime_deadline = fields.Datetime.from_string(datetime_deadline)
        now = datetime.now(UTC).replace(tzinfo=None)
        if datetime_deadline < now:
            return 'overdue'
        elif (datetime_deadline.date() == now.date()):
            return 'today'
        else:
            return 'planned'