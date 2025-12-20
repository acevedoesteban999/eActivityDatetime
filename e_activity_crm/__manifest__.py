# -*- coding: utf-8 -*-
{
    'name': 'E Activity CRM',
    'version': '19.6.0',
    'summary': "Edit CRM for Activity Datetime ",
    'description':  "Add automatic activity creation upon lead creation based on configuration."
                    "Add periodic activity regeneration for CRM leads based on stage configuration.",
    'author': 'esteban.acevedo@qa-bit.com',
    'website': '',
    'category': '',
    'depends': ['base', 'web' , 'crm', 'e_activity_datetime', 'mail' ],
    'data': [
        "data/cron.xml",
        
        "views/res_config_settings.xml",  
        "views/mail_activity.xml",
        "wizard/mail_activity_schedule.xml",
        
    ],
    'assets':{
        'web.assets_backend':[
            'e_activity_crm/static/src/components/**/*',
        ],
    },
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
