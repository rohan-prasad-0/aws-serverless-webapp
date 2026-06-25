import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Contact')

# HTML page loaded from file inside ZIP
with open('index.html', 'r', encoding='utf-8') as f:
    HTML_PAGE = f.read()

def lambda_handler(event, context):

    method = event.get('httpMethod')


    # SHOW WEB PAGE (GET /)

    if method == 'GET':
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/html'
            },
            'body': HTML_PAGE
        }


    # SAVE DATA (POST /save)

    if method == 'POST':

        body = json.loads(event['body'])

        table.put_item(
            Item={
                'id': str(uuid.uuid4()),
                'name': body['name'],
                'email': body['email'],
                'message': body['message']
            }
        )

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'Message sent successfully'
            })
        }

    return {
        'statusCode': 405,
        'body': 'Method Not Allowed'
    }