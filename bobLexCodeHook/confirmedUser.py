import base64
import json
import os
import urllib
from urllib import request, parse

TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_API_KEY = os.environ.get("TWILIO_API_KEY")
TWILIO_API_SECRET = os.environ.get("TWILIO_API_SECRET")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")
TWILIO_SMS_URL = "https://api.twilio.com/2010-04-01/Accounts/{}/Messages.json"

def confirmedUserHandler(event, context):
    for record in event.get('Records'):
        if (record.get('eventName') == 'REMOVE'):
            print (record)
            code = record.get('dynamodb').get('OldImage').get('code').get('S')
            to_number = record.get('dynamodb').get('OldImage').get('phone').get('S')
    
            # Create message
            body = "Hi, thx for the access....what can I do for you?"

            send_sms(to_number, body)
    
def send_sms(to_number, body):
    # insert Twilio Account SID into the REST API URL
    populated_url = TWILIO_SMS_URL.format(TWILIO_ACCOUNT_SID)
    post_params = {"To": to_number, "From": TWILIO_PHONE_NUMBER, "Body": body}
 
    # encode the parameters for Python's urllib
    data = parse.urlencode(post_params).encode()
    req = request.Request(populated_url)
 
    # add authentication header to request based on Account SID + Auth Token
    authentication = "{}:{}".format(TWILIO_API_KEY, TWILIO_API_SECRET)
    base64string = base64.b64encode(authentication.encode('utf-8'))
    req.add_header("Authorization", "Basic %s" % base64string.decode('ascii'))
 
    try:
        # perform HTTP POST request
        with request.urlopen(req, data) as f:
            print("Twilio returned {}".format(str(f.read().decode('utf-8'))))
    except Exception as e:
        # something went wrong!
        return e