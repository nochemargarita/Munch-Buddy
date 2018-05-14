import os
from twilio.rest import Client

ACCOUNT_SID = os.environ['ACCOUNT_SID']
AUTH_TOKEN = os.environ['AUTH_TOKEN']
MY_CELL = os.environ['MY_CELL']
MY_TWILIO = os.environ['MY_TWILIO']

client = Client(ACCOUNT_SID, AUTH_TOKEN)

my_message = 'Hello...'

message = client.messages.create(from_=MY_TWILIO, to=MY_CELL, body=my_message)
print 'message sent'
