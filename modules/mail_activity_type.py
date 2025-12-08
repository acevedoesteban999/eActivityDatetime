from odoo import models,fields,api
from dateutil.relativedelta import relativedelta
class MailActivityType(models.Model):
    _inherit = "mail.activity.type"
    
    
    def _get_datetime_deadline(self):
        self.ensure_one()
        # activity_previous_deadline
        if self.delay_from == 'previous_activity' and self.env.context.get('activity_previous_datetime_deadline'):
            base = fields.Datetime.from_string(self.env.context.get('activity_previous_datetime_deadline'))
        else:
            base = fields.Datetime.now().replace(second=0)
        return base + relativedelta(**{self.delay_unit: self.delay_count})