import boto3
import botocore
import json
import decimal
from datetime import date

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

PENDING = 'Pending'
USERS_TABLE = 'usersTable'

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
            if not item:
                value = item[field]
            else:
                raise Exception("Exception: Empty record or field for {} from {}.".format(field,userPhoneNum))
        except Exception as e:
            print(e.message)
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

def getPendingAuth(code,token):
    value=""
    table = dynamodb.Table(USERS_TABLE)
    try:
        response = table.update_item(
            Key={
                'access_token': code
            },
            UpdateExpression="set access_token=:t",
            ExpressionAttributeValues={
                ':t': token
            },
            ReturnValues="UPDATED_EXISTING"
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
            print(e.message)