# eActivityCRM 
### (e_activity_crm)

**Automatic & Recurring Activities for CRM Leads**  
*Odoo 19 *

---
Whenever a lead is created, the system instantly schedules the activity you configured (type + local time) and, if desired, keeps cloning it at the interval you set until the lead moves out of the chosen stage.
---

## Key Features

- **Create lead with activity  :**: Generates a new activity when creating the lead 
![IMAGE](static/description/assets/screenshots/1.png)
- **Generic:** Pick activity type, due-time and repetition for automatic activity creation
![IMAGE](static/description/assets/screenshots/2.png)
- **Timezone aware:**  The due hour is always shown in the user’s timezone; daylight-saving is handled by Odoo’s core. 
- **Stage-gated recurrence:** A new “Allow recurring activities” checkbox is added to CRM stages – only leads in those stages can receive periodic copies. 
![IMAGE](static/description/assets/screenshots/3.png)
<br/>

![IMAGE](static/description/assets/screenshots/3-1.png)
-**Immutable history:**  Once an activity is repeated (cloned) the original becomes read-only (`repeated = True`) so your audit trail is safe. 
![IMAGE](static/description/assets/screenshots/4.png)
![IMAGE](static/description/assets/screenshots/5.png) 
- **Cron driven:** A lightweight cron job (`ir.cron`) looks every configurated minutes for activities that match: `active = True, res_model = 'crm.lead', is_periodic = True, repeated = False, repetition_period_days > 0` and duplicates them.