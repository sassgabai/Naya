import json
import boto3

def generate_bedrock_client():
    
    bedrock_client = boto3.client(
        service_name='bedrock-runtime',
        region_name='eu-central-1', 
        endpoint_url='https://frankfurt.chatbot.bedrock.com',
        verify=False
    )
    
    kwargs = {
        'modelId': 'anthropic.claude-3-sonnet-20240229-v1:0',
        'accept': 'application/json',
        'contentType': 'application/json',
    }
    
    
    return bedrock_client, kwargs