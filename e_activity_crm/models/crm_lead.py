from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime,UTC
from datetime import timedelta
class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.model_create_multi
    def create(self, vals_list):
        leads = super().create(vals_list)

        ICP = self.env['ir.config_parameter'].sudo()
        is_activity_on_create = bool(ICP.get_param('crm_lead_auto_activity.is_auto_create_activity', default=False))
        if not is_activity_on_create:
            return leads
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
            
        activity_type_id = int(ICP.get_param('crm_lead_auto_activity.auto_lead_activity_type_id', default=0))
        if not activity_type_id:
            return leads
        try:
            periodic_vals = {
                'is_periodic': bool(ICP.get_param('crm_lead_auto_activity.auto_is_periodic', default=False)),
                'repetition_period_days': int(ICP.get_param('crm_lead_auto_activity.auto_repetition_period_days_days', default=0)),
            }
        except:
            periodic_vals = {}
        activity_type = self.env['mail.activity.type'].browse(activity_type_id).exists()
        if not activity_type:
            raise UserError(_('The default activity type configured in CRM settings no longer exists.'))
        
        activities = [{
            'res_id': lead.id,
            'res_model_id': self.env['ir.model']._get_id('crm.lead'),
            'activity_type_id': activity_type.id,
            'summary': _("Discovery Call") ,
            'note': _('This is an automatic activity created upon lead start.'),
            'date_deadline': fields.Date.context_today(self),
            'datetime_deadline': deadline_datetime,
            'all_day':False,
            'user_id': lead.user_id.id or self.env.user.id,
            **periodic_vals,
            
        } for lead in leads]
        
        self.env['mail.activity'].create(activities)

        return leads
    
    
    def _cron_regenerate_repetitive_activities(self):
        activities = self.env['mail.activity'].search([
            ('active','=',True),
            ('res_model','=','crm.lead'),
            ('is_periodic','=',True),
            ('repeated','=',False),
            ('repetition_period_days','>',0),
        ]).filtered(lambda rec: rec.state == 'overdue' and rec.in_crm_stage)
        
        for activity in activities:
            activity.copy({
                'datetime_deadline': activity.datetime_deadline + timedelta(days=activity.repetition_period_days),
                'date_deadline': activity.date_deadline + timedelta(days=activity.repetition_period_days),
                'note': f"[{_('REPEATED')}]" + activity.note,
            })
            activity.repeated = True,
            activity.env.cr.commit()