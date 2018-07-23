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
    token = event["pathParameters"]["token"]

    getPendingAuth(code,token)
    
    return {
        'statusCode': 200,
        'body': json.dumps("{'code': code,'token': token}")
    }