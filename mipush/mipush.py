#!/usr/bin/env python

from base.APIMessage import PushMessage
from APISender import APISender
from base.APIConstants import Constants

APP_SECRET = '*****************************'

RECIEVER_ALIAS = '**********************'

def sendMessage(title, description, payload, notify_id=1):
    message = PushMessage() \
        .restricted_package_name('com.reckmi.mipush') \
        .title(title).description(description) \
        .pass_through(0).payload(payload) \
        .notify_type(5).notify_id(notify_id) \
        .extra({Constants.extra_param_notify_effect:Constants.notify_launcher_activity})

    sender = APISender(APP_SECRET)

    recv = sender.send_to_alias(message.message_dict(), RECIEVER_ALIAS)
    print recv
    
    
if __name__ == "__main__":
    sendMessage("Test", "test", "nihao")
