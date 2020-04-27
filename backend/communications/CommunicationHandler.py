import json

import requests
from django.core.mail import send_mail

from communications.Message import construct_message
from hcwtracker import settings


class CommunicationHandler:

    def __init__(self):
        super()

    def send_message(self, user, message_type, extra, communication_type="all", *args, **kwargs):
        message = construct_message(message_type, user, extra)
        if communication_type == "all":
            self.send_whatsapp_message(user, message)
            self.send_telegram_message(user, message)
            self.send_email_message(user, message)
        pass

    def send_whatsapp_message(self, user, message):
        if user.whatsapp_number is not None:
            url = settings.INFOBIP_URL
            headers = {'content-type': 'application/json',
                       'Authorization': 'App '+settings.INFOBIP_TOKEN}
            body = {"destinations": [{"to": {"phoneNumber": user.whatsapp_number}}],
                    "whatsApp": {
                        "text": message["message"]}}
            r = requests.post(url, data=json.dumps(body), headers=headers)

    def send_telegram_message(self, user, message):
        pass

    def send_email_message(self, user, message):
        if message["header"] is not None:
            send_mail(
                message["header"],
                message["message"],
                settings.EMAIL_HOST_USER,
                [user["email"]],
                fail_silently=True,
            )
