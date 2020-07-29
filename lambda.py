'''
Create dynamodb table for Queue
Click manage stream
Select Keys only and then enable
Copy Latest stream ARN
Create IAM role called lambda-dynamo with lambdafullaccess and dynamofullaccess
Add to a new lambda function with lambda-dynamo role
Click Add trigger
Select DynamoDB
Paste ARN in DynamoDB table
Copy the following function to the function code.
'''
import json
import boto3

dynamo = boto3.client('dynamodb')
client = boto3.client('sns')

def lambda_handler(event, context):
    users = dynamo.scan(TableName="hackathon-db")["Items"]
    if len(users) < 2:
        return {
        'statusCode': 200,
        'body': json.dumps('Insuffecient Members')
    }
    p1 = {'Number': users[0]['Number']['S'],'Name': users[0]['Name']['S']}
    p2 = {'Name': users[1]["Name"]['S'], 'Number': users[1]["Number"]['S']}
    dynamo.delete_item(TableName="hackathon-db", Key={"Number":{'S':p1['number']}})
    dynamo.delete_item(TableName="hackathon-db", Key={"Number":{'S':p2['number']}})
    client.publish(PhoneNumber = p1['Number'], Message="You have been matched with " + p2['Name'] + ". You can text them at "+ p2['Number'] + ".")
    client.publish(PhoneNumber = p2['Number'], Message="You have been matched with " + p1['Name'] + ". You can text them at "+ p1['Number'] + ".")
    return {
        'statusCode': 200,
        'body': json.dumps(users[0])
    }


'''
Create table for users names
Add that table name to hello_world.py lines 56 and 67
Create table for users phones
Add table name to hello_world.py lines 43 and 74
Add table name for queue to hello_world.py line 81

zip contents of skill_env (not the folder itself)
create new lambda for the alexa skill
Click Actions then Upload a .zip file
Select the created zip

Click permissions under the title of the lmabda function
Click edit on the right of execution role
Paste 'lambda_function.lambda_handler' into handler
Copy ARN at the top of the page

Go to Alexa Console
Open add_to_db
Under build click endpoint
Paste the lambda ARN under each region
'''