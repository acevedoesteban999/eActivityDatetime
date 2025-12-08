# -*- coding: utf-8 -*-
{
    'name': 'Activity DateTime',
    'version': '19.0.0.1',
    'summary': """ Activity DateTime """,
    'author': 'esteban.acevedo@qa-bit.com, acevedoesteban999@gmail.com',
    'website': '',
    'category': '',
    'depends': ['base', 'mail','web'],
    'data': [
        "wizard/mail_activity_schedule.xml",  
        "views/mail_activity.xml",
    ],
    'assets':{
        'web.assets_backend':[
            'activity_datetime/static/src/core/web/*',
        ],
    },
    
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
