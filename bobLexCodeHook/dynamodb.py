import boto3
import botocore
import json
import decimal
from datetime import date
import random
import uuid

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

PENDING = 'Pending'
USERS_TABLE = 'usersTable'
AUTH_REQUESTS_TABLE = 'authRequest'
EVENTS_TABLE = 'event'

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def getCurrentUser(intent_request,field):
    value=""
    userPhoneNum = intent_request['userId']
    table = dynamodb.Table(USERS_TABLE)
    try:
        response = table.get_item(
            Key={
                'phone': userPhoneNum
            }
        )
    except botocore.exceptions.ClientError as e:
        print(e.response['Error']['Message'])
        raise Exception("Exception: Can't retrieve record for {} from {}.".format(field,userPhoneNum))
    else:
        try:
            item = response['Item']
            if item:
                value = item[field]
            else:
                raise Exception("Exception: Empty record or field for {} from {}.".format(field,userPhoneNum))
        except Exception as e:
            print(e)
            #raise Exception("Exception: Can't retrieve {} from {}.".format(field,userPhoneNum))
            
    return value

def updateUser(phone,fname,token):
    value=""
    table = dynamodb.Table(USERS_TABLE)
    try:
        response = table.update_item(
            Key={
                'phone': phone
            },
            UpdateExpression="set fname = :f, access_token=:t",
            ExpressionAttributeValues={
                ':f': fname,
                ':t': token
            },
            ReturnValues="UPDATED_NEW"
        )
    except botocore.exceptions.ClientError as e:
        print(e.response['Error']['Message'])

def addUser(phone_num):
    value=""
    table = dynamodb.Table(USERS_TABLE)
    try:
        response = table.put_item(
            Item={
                'phone': phone_num,
                'expiration': str(date.today().strftime('%dm-%d-%y')),
                'access_token': PENDING,
                'token_type': 'bearer',
                'fname': PENDING
            }
        )
    except botocore.exceptions.ClientError as e:
        print(e.response['Error']['Message'])
    else:
        try:
            item = response['Item']
        except Exception as e:
            print(e)

def addAuthRequest(phone):
    print("begin addAuthRequest")
    table = dynamodb.Table(AUTH_REQUESTS_TABLE)
    try:
        code = random.SystemRandom().randint(1000, 10000000)
        
        response = table.put_item(
            Item={
                'code': int(code),
                'phone': str(phone)
            }
        )
        return code
    except botocore.exceptions.ClientError as e:
        print(e.response['Error']['Message'])

def getPhoneFromAuthRequests(code):
    value = ""
    table = dynamodb.Table(AUTH_REQUESTS_TABLE)
    try:
        response = table.get_item(
            Key={
                'code': int(code)
            }
        )
    except botocore.exceptions.ClientError as e:
        print(e.response['Error']['Message'])
        raise Exception("Exception: Can't retrieve record for {}.".format(code))
    else:
        try:
            item = response['Item']
            if item:
                value = item['phone']
            else:
                raise Exception("Exception: Empty record or field for {}.".format(code))
        except Exception as e:
            print(e.message)
            
    return value

def deletePendingAuth(code):
    table = dynamodb.Table(AUTH_REQUESTS_TABLE)
    try:
        response = table.delete_item(
            Key={
                'code': int(code)
            }
        )
    except botocore.exceptions.ClientError as e:
        print(e.response['Error']['Message'])
        raise Exception("Exception: Can't delete record for {}.".format(code))
        
def addEvent(message):
    
    table = dynamodb.Table(EVENTS_TABLE)
    try:
        response = table.put_item(
            Item={
                'transId': str(uuid.uuid4()),
                'message': message
            }
        )
    except botocore.exceptions.ClientError as e:
        print(e.response['Error']['Message'])
