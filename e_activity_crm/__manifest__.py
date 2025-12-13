# -*- coding: utf-8 -*-
{
    'name': 'E Activity CRM',
    'version': '19.4.1',
    'summary': "Edit CRM for Activity Datetime ",
    'description':  "Add automatic activity creation upon lead creation based on configuration."
                    "Add periodic activity regeneration for CRM leads based on stage configuration.",
    'author': 'acevedoesteban999@gmail.com,esteban.acevedo@qa-bit.com',
    'website': 'https://acevedoesteban999/eActivity',
    'category': '',
    'depends': ['base', 'web' , 'crm', 'e_activity_datetime', 'mail' ],
    'data': [
        "data/cron.xml",
        
        "views/res_config_settings.xml",  
        "views/mail_activity.xml",
        "views/crm_stage.xml",
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
