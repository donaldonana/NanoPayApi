# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
<<<<<<< HEAD

=======
client = Client(account_sid, auth_token)
>>>>>>> 19b0bdf81f71656457920994b7d6f7864e2c1a5c
message = client.messages \
                .create(
                     body="VOTRE CODE DE VERIFICATION EST : 1234.",
                     from_='+16672223508',
                     to='+23765601533'
                 )

print(message)