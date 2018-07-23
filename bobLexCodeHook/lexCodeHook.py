import math
import datetime
import time
import os
import logging
from dynamodb import *
from teamsnap import *
from lex_utils import *
from utils import *

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

""" --- Main handler --- """
def requestHandler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    # By default, treat the user request as coming from the America/New_York time zone.
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event)

""" --- Intents --- """
def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'GreetingForTeamAssistant':
        return teamAssistantGreeting(intent_request)
    if intent_name == 'CheckTeamsnapAccess':
        return teamAssistantConnectivityCheck(intent_request)
    if intent_name == 'UpdateMyInfo':
        return updateUserInfoFromTeamsnap(intent_request)
    
    raise Exception('Intent with name ' + intent_name + ' not supported')

""" --- Functions that control the bot's behavior --- """
def teamAssistantGreeting(intent_request):
    message=""
    userPhoneNum = intent_request['userId']
    try:
        fname=getCurrentUser(intent_request,"fname")
        expiration=getCurrentUser(intent_request,"expiration")
    
        if fname == PENDING:
            message = "I'm still waiting for your name from Teamsnap, I'll let you know when it comes in.  Looks like you have been waiting since {}".format(expiration)                
        elif len(fname)>0:
            message = 'Hi {}, what can I do for you?'.format(fname)
        else:
            addUser(userPhoneNum)
            message = 'Hi, please click this link to authorize me to your Teamsnap account: https://d3bbtrhm68u3kt.cloudfront.net/index.html'
    except Exception as e:
        print(e.message)
        message = "I'm sorry...must be catching a cold, I feel a little off.  Please try again in a few minutes."
        
    return close(intent_request['sessionAttributes'],
            'Fulfilled',
            {'contentType': 'PlainText',
            'content': message})