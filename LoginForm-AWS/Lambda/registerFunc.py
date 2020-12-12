import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    print("event input in registerFunc: ", event)
    emailMessage = event['email']
    passwordMessage = event['password']
    appendAddUserToDynamodb(emailMessage,passwordMessage)
    return {
        'statusCode': 200,
        #'body': json.dumps('Hello from Lambda!')
        'body' : json.dumps([emailMessage,passwordMessage])
    }



def appendAddUserToDynamodb(email,password):
    dynamo_client = boto3.resource('dynamodb') #create dynamoDB client
    usersTable = dynamo_client.Table('usersDynamo') #call the dynamoDB table
    user = {"email":email,"password":password} #create user with details
    usersTable.put_item(Item=user) #add user to dynamoDB