from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.addons.e_activity_datetime.utils.date import get_server_utc_datetime
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

        deadline_datetime = get_server_utc_datetime(h,m)
        
        activity_type_id = int(ICP.get_param('crm_lead_auto_activity.auto_lead_activity_type_id', default=0))
        if not activity_type_id:
            return leads

        activity_type = self.env['mail.activity.type'].browse(activity_type_id).exists()
        if not activity_type:
            raise UserError(_('The default activity type configured in CRM settings no longer exists.'))

        activities = [{
            'res_id': lead.id,
            'res_model_id': self.env['ir.model']._get_id('crm.lead'),
            'activity_type_id': activity_type.id,
            'summary': _("Discovery Call") ,
            'note': _('This is an automatic activity created upon lead creation.'),
            'date_deadline': fields.Date.context_today(self),
            'datetime_deadline': deadline_datetime,
            'all_day':False,
            'user_id': lead.user_id.id or self.env.user.id,
        } for lead in leads]
        
        self.env['mail.activity'].create(activities)

        return leads
    
    
    def _cron_regenerate_repetitive_activities(self):
        activities = self.env['mail.activity'].search([
            ('active','=',True),
            ('res_model','=','crm.lead'),
            ('is_periodic','=',True),
            ('repeated','=',False),
            ('repetition_period','>',0),
        ]).filtered(lambda rec: fields.Datetime.now() > rec.datetime_deadline and rec.in_crm_stage)
        
        for activity in activities:
            activity.copy({
                'datetime_deadline': activity.datetime_deadline + timedelta(days=activity.repetition_period),
                'date_deadline': activity.date_deadline + timedelta(days=activity.repetition_period),
            })
            activity.repeated = True,
            activity.env.cr.commit()