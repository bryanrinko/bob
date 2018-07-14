from botocore.vendored import requests
from datetime import date
from dynamodb import *
from lex_utils import *
import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

TEAMSNAP_BASE_URL = 'https://api.teamsnap.com/v3/'
TEAMSNAP_ME_URL = 'https://api.teamsnap.com/v3/me'

def updateUserInfoFromTeamsnap(intent_request):
    message=''
    try:
        token = getCurrentUser(intent_request,"access_token")
        phone = getCurrentUser(intent_request,"phone")
        
        result = requests.get(TEAMSNAP_ME_URL, headers={'content-type': 'application/json', 'Authorization': 'Bearer {}'.format(token)})
        result.raise_for_status()
        logging.info('teamsnap-url - OK')
        jsonObj = json.loads(result.text)
        fname=jsonObj['collection']['items'][0]['data'][8]['value']
        updateUser(phone,fname,token)
        message='{} updated!'.format(fname)
    except requests.exceptions.RequestException as e:
        logger.error("ERROR: Request Error: %s" % e)
        message='Boo...update failed!'
        
    return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': message})

def teamAssistantConnectivityCheck(intent_request):
    message=''
    try:
        token = getCurrentUser(intent_request,"access_token")
        
        result = requests.get(TEAMSNAP_BASE_URL, headers={'content-type': 'application/json', 'Authorization': 'Bearer {}'.format(token)})
        result.raise_for_status()
        logging.info('teamsnap-url - OK')
        print (result.text)
        #collection = Collection.from_json(result.text)
        jsonObj = json.loads(result.text)
        message = 'Good to go'
    except requests.exceptions.RequestException as e:
        logger.error("ERROR: Request Error: %s" % e)
        message = "Ran into an issue...bummer"
        
    return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': message})