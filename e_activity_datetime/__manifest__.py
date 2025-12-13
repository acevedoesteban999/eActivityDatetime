# -*- coding: utf-8 -*-
{
    'name': 'E Activity DateTime',
    'version': '19.3.1',
    'summary': """ Activity DateTime """,
    'author': 'acevedoesteban999@gmail.com , esteban.acevedo@qa-bit.com',
    'website': 'https://acevedoesteban999/eActivity',
    'category': '',
    'depends': ['base', 'mail','web'],
    'data': [
        "wizard/mail_activity_schedule.xml",  
        "views/mail_activity.xml",
    ],
    'assets':{
        'web.assets_backend':[
            'e_activity_datetime/static/src/core/web/*',
            'e_activity_datetime/static/src/components/**/*',
        ],
    },
    
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
