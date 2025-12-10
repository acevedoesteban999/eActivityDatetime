from odoo import models,fields,api

class MailActivity(models.Model):
    _inherit = 'mail.activity'
    
    datetime_deadline = fields.Datetime('Due Date Time',readonly=False,store=True,compute="_compute_datetime_deadline",index=True,default=fields.Datetime.now().replace(second=0))
    date_deadline = fields.Date('Due Date',store=True,readonly=False,compute="_compute_date_deadline", index=True, required=True, default=fields.Date.context_today)
    all_day = fields.Boolean("All Day",default=True)
    
    @api.depends('datetime_deadline')
    def _compute_date_deadline(self):
        for rec in self:
            if not rec.all_day and rec.datetime_deadline:
                rec.date_deadline =  rec.datetime_deadline.date()
            else:
                rec.date_deadline = rec.date_deadline or fields.Date.today()

    @api.depends('date_deadline')
    def _compute_date_deadline(self):
        for rec in self:
            if rec.all_day and rec.date_deadline:
                rec.datetime_deadline =  rec.date_deadline.start_of('day')
            else:
                rec.datetime_deadline = rec.datetime_deadline or fields.Datetime.now().replace(second=0)
                
    def _to_store_defaults(self, target):
        return super()._to_store_defaults(target) + ['datetime_deadline','all_day']