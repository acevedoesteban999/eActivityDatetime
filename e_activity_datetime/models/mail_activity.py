from odoo import models,fields,api,exceptions , _
from datetime import datetime,UTC
from pytz import timezone as pytz_timezone,UTC as pytz_UTC
class MailActivity(models.Model):
    _inherit = 'mail.activity'
    
    datetime_start = fields.Datetime('Start DateTime',readonly=False,store=True,compute="_compute_datetime_deadline",index=True)
    datetime_deadline = fields.Datetime('Due DateTime',readonly=False,store=True,compute="_compute_datetime_deadline",index=True,default=fields.Datetime.now().replace(second=0))
    datetime_duration = fields.Float("Datetime Duration",compute="_compute_datetime_duration")
    date_deadline = fields.Date('Due Date',store=True,readonly=False,compute="_compute_date_deadline", index=True, required=True, default=fields.Date.context_today)
    datetime_calendary = fields.Datetime(store=True,compute="_compute_datetime_calendary")
    all_day = fields.Boolean("All Day",default=True)
    
    @api.depends('datetime_start','date_deadline','datetime_deadline')
    def _compute_datetime_calendary(self):
        for rec in self:
            if rec.all_day:
                rec.datetime_calendary = rec.date_deadline or rec.datetime_deadline.date()
            else:
                rec.datetime_calendary = rec.datetime_start if rec.datetime_start else rec.datetime_deadline
    
    @api.constrains('datetime_start','datetime_deadline')
    def check_datetimes(self):
        for rec in self:
            if not rec.all_day and rec.datetime_start and rec.datetime_start > rec.datetime_deadline:
                raise exceptions.UserError(_("Datetime start can not be after datetime end"))
    
    @api.depends('datetime_start','datetime_deadline')
    def _compute_datetime_duration(self):
        for rec in self:
            if rec.datetime_deadline and rec.datetime_start:
                rec.datetime_duration = (rec.datetime_deadline - rec.datetime_start).total_seconds() / 3600.0
            else:
                rec.datetime_duration = 0
    
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
                rec.datetime_start = rec.datetime_deadline = datetime.now(UTC).replace(hour=6,minute=0,second=0,tzinfo=None)
                
            else:
                rec.datetime_deadline = rec.datetime_deadline or fields.Datetime.now().replace(second=0)
                #rec.datetime_start = rec.datetime_start or rec.datetime_deadline
                
    def _to_store_defaults(self, target):
        return super()._to_store_defaults(target) + ['datetime_start','datetime_deadline','all_day']
    
    
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
        deadline = fields.Datetime.from_string(datetime_deadline)
        
        if tz:
            tz_obj = pytz_timezone(tz) if isinstance(tz, str) else tz
        else:
            tz_obj = UTC
        
        deadline= deadline.astimezone(tz_obj)
        now = datetime.now(tz_obj).replace(microsecond=0)
        if deadline < now:
            return 'overdue'
        elif (deadline.date() == now.date()):
            return 'today'
        else:
            return 'planned'