from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime,UTC
from datetime import timedelta
class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.model_create_multi
    def create(self, vals_list):
        leads = super().create(vals_list)
        for lead in leads:
            if lead.type != 'lead':
                continue
            ICP = self.env['ir.config_parameter'].sudo()
            is_activity_on_create = bool(ICP.get_param('crm_lead_auto_activity.is_auto_create_activity', default=False))
            if not is_activity_on_create:
                continue
            
            activity_type_id = int(ICP.get_param('crm_lead_auto_activity.auto_lead_activity_type_id', default=0))
            if not activity_type_id:
                continue
            
            auto_lead_time_str = ICP.get_param('crm_lead_auto_activity.auto_lead_time_deadline', default='7.0')
            try:
                h = int(float(auto_lead_time_str))
                m = int(round((float(auto_lead_time_str) - h) * 60))
            except ValueError:
                h, m = 8, 0

            now = datetime.now(UTC).replace(tzinfo=None)
            deadline_datetime = now.replace(hour=h,minute=m,second=0)
            if deadline_datetime < now:
                deadline_datetime += timedelta(days=1)
                
            activity_type = self.env['mail.activity.type'].browse(activity_type_id).exists()
            if not activity_type:
                raise UserError(_('The default activity type configured in CRM settings no longer exists.'))
            
            activity = {
                'res_id': lead.id,
                'res_model_id': self.env['ir.model']._get_id('crm.lead'),
                'activity_type_id': activity_type.id,
                'summary': _("Discovery Call") ,
                'note': _('This is an automatic activity created upon lead start.'),
                'date_deadline': fields.Date.context_today(self),
                'datetime_deadline': deadline_datetime,
                'all_day':False,
                'user_id': lead.user_id.id or self.env.user.id,
                'is_rescheduled':True,
                'reschedule_days': 1,   
            }
            
            self.env['mail.activity'].create(activity)

        return leads
    
    
    def _cron_regenerate_repetitive_activities(self):
        activities = self.env['mail.activity'].search([
            ('active','=',False),
            ('res_model','=','crm.lead'),
            ('is_rescheduled','=',True),
            ('done_reschedule','=',False),
        ])
        
        for activity in activities.filtered(lambda rec: rec.crm_type == 'lead'):
            datetime_done = activity.datetime_deadline.replace(
                year = activity.date_done.year,
                month = activity.date_done.month,
                day = activity.date_done.day,
                ) + timedelta(days=activity.reschedule_days)
            activity.copy({
                'active':True,
                'datetime_deadline': datetime_done,
                'date_deadline': datetime_done,
                'note':  activity.note,
            })
            activity.done_reschedule = True
            activity.env.cr.commit()