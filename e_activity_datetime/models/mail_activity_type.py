from odoo import models,fields,api
from dateutil.relativedelta import relativedelta
class MailActivityType(models.Model):
    _inherit = "mail.activity.type"
    
    
    def _get_datetime_deadline(self):
        self.ensure_one()
        base = fields.Datetime.now().replace(second=0)
        return base + relativedelta(**{self.delay_unit: self.delay_count})