import json
import boto3
from get_subject import llm_result
from llm_result import get_answer, get_default_answer
from bedrock_client import generate_bedrock_client


def lambda_handler(event, context):
    
    body = json.loads(event['body']) if 'body' in event else event 
    
    bedrock_client, kwargs = generate_bedrock_client()
    
    question = body['question']
    
    get_subject = llm_result(question, bedrock_client, kwargs)
 
    answer = get_default_answer(bedrock_client, kwargs) if get_subject == 'NoSuchKey' else get_answer(question, get_subject, bedrock_client, kwargs)
    
    return {
        'statusCode': 200,
        'body': json.dumps({'results':answer}),
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
        
    }
