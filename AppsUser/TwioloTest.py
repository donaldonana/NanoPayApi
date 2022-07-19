# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)


def SendCode(phone='+237656015433') :
    try:
        message = client.messages.create(
                        body="VOTRE CODE DE VERIFICATION EST : 1234.",
                        from_='+16672223508',
                        to=phone
                    )
        print(message)
    except :
        print("SomeThing")


