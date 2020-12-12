import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    # TODO implement
    print("event input in loginFunc: ", event)
    emailMessage = event['email']
    passwordMessage = event['password']

    isValidUser = verifyUser(emailMessage,passwordMessage)

    #username and password matches
    if(isValidUser):
        response_body = {}
        response_body["email"] = emailMessage
        response_body["password"] = passwordMessage
        return{
            'statusCode' : 200,
            'body' : response_body
        }
    else:
        return{
        'statusCode': 400,
        #'statusCode': 200,
        'body': "Email/Password is incorrect"
        }

    
    #return {
    #    'statusCode': 200,
    #    #'body': json.dumps('Hello from Lambda!')
    #    'body' : json.dumps([emailMessage,passwordMessage])
    #}
    

def verifyUser(enteredEmail,enteredPassword):
    dynamo_client = boto3.resource('dynamodb') #create dynamoDB client
    usersTable = dynamo_client.Table('usersDynamo') #call the dynamoDB table
    print("enteredEmail:{0},enteredPassword:{1}".format(enteredEmail,enteredPassword))

    #query dynamoDB for the email
    #responseData = usersTable.query(IndexName="otp-index", KeyConditionExpression=Key('otp').eq(str(event['message'])))
    responseData = usersTable.query(KeyConditionExpression=Key('email').eq(enteredEmail))
    print('responseData: ', responseData) 
    #{'Items': [{'email': 'abc@gmail.com', 'password': 'value2'}], 'Count': 1, 'ScannedCount': 1,... if email matches
    #{'Items': [], 'Count': 0, 'ScannedCount': 0, ... if email doesn't match any on table

    if(responseData["Count"] == 0): #no items on query return list (no valid email registered)
        return False
    else: #email is registered, check if password is correct
        realPassword = responseData["Items"][0]["password"]
        print("realPassword: ", realPassword)
        if(realPassword == enteredPassword):
            createUserSession = True
        else:
            createUserSession = False

        return createUserSession
    

"""
response = table.query(
    KeyConditionExpression=Key('year').eq(1985)
)

for i in response['Items']:
    print(i['year'], ":", i['title'])
"""
