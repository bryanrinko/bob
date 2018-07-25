import json
from dynamodb import *
from teamsnap import *

""" --- Main handler --- """
def samlSaveHandler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    code = event["pathParameters"]["code"]
    print(code)
    token = event["pathParameters"]["token"]
    print(token)
    phone = getPhoneFromAuthRequests(code)
    print (phone)
    addUser(phone)
    updateDBUserInfoFromTeamsnap(token,phone)
    deletePendingAuth(code)
    
    return {
        'statusCode': 200,
        'body': {'message':'Got it'}
    }