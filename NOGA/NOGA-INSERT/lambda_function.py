import json
from secret import get_secret
from posgres import insert_postgres


def lambda_handler(event, context):
    
    body = json.loads(event['body']) if 'body' in event else event
    
    secret = get_secret()
    
    insert_postgres(secret, body)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello')
    }
