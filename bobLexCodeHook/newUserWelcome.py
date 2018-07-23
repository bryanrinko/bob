import base64
import json
import os
from twilio.rest import Client

TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_API_KEY = os.environ.get("TWILIO_API_KEY")
TWILIO_API_SECRET = os.environ.get("TWILIO_API_SECRET")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")


def newUserHandler(event, context):
    event.Records.forEach((record) => {
        console.log('Stream record: ', JSON.stringify(record, null, 2));
        
        for record in event.get('Records'):
            if (record.get('eventName') == 'MODIFY'):
                if (record['OldImage']['access_token']['S'] == 'Pending' && record['NewImage']['access_token']['S'] != 'Pending'):
                    to_number = record['NewImage']['phone']['S']
    
                    # Create message
                    body = "Hey, thx for the access....what can I do for you?"

                    send_sms(to_number, body)

    return "SMS sent successfully!"
    
def send_sms(to_number, body):
    client = Client(TWILIO_API_KEY, TWILIO_API_SECRET, TWILIO_ACCOUNT_SID)
    client.api.messages.create(to_number,
                           from_=TWILIO_PHONE_NUMBER,
                           body=body)