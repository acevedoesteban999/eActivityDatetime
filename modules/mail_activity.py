from odoo import models,fields,api

class MailActivity(models.Model):
    _inherit = 'mail.activity'
    
    datetime_deadline = fields.Datetime('Due Date',index=True,default=fields.Datetime.now().replace(second=0))
    date_deadline = fields.Date('Due Date',store=True,compute="_compute_date_deadline", index=True, required=True, default=fields.Date.context_today)
    all_day = fields.Boolean("All Day",default=True)
    
    @api.depends('datetime_deadline')
    def _compute_date_deadline(self):
        for rec in self:
            rec.date_deadline =  not rec.all_day and rec.datetime_deadline and rec.datetime_deadline.date() or rec.date_deadline or  fields.Date.today()

    
    def _to_store_defaults(self, target):
        return super()._to_store_defaults(target) + ['datetime_deadline','all_day']