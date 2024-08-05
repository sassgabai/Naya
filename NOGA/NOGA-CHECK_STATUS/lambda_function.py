import json
from secret import get_secret
from postgres import get_status


def lambda_handler(event, context):
    
    body = json.loads(event['body']) if 'body' in event else event
    
    secret = get_secret()
    
    answer = get_status(secret, body)

    return {
        'statusCode': 200,
        'body': answer
    }
