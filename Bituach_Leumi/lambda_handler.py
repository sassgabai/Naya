import json
import boto3
from claude import claude_system_prompt
from llm import llm_answer, llm_unhandled_answer, llm_summarize, llm_system_result
from bedrock_client import generate_bedrock_client


def lambda_handler(event, context):
    body = json.loads(event['body']) if 'body' in event else event

    bedrock_client, kwargs = generate_bedrock_client()

    question = body['question']

    # capture history
    history = body['history'] if 'history' in body else []
    history_list = list(map(lambda x: x['type'] + ": " + x['value'], history))

    # get only the system_prompt
    get_system_prompt = claude_system_prompt('')
    get_system_prompt = get_system_prompt['messages'][0]['content'][0]['text'].split('question:')[0]

    # get summary of previous conversation and send to llm for a response of the relevant context
    get_summary_history = llm_summarize(question, history_list, get_system_prompt, bedrock_client, kwargs)

    # get_subject = llm_result(question, bedrock_client, kwargs)

    answer = llm_unhandled_answer(question, bedrock_client, kwargs) if 'NoSuchKey' in get_summary_history \
        else llm_answer(question, get_summary_history, bedrock_client, kwargs)

    # to fix issue where answer gets "NoSuchKey" error
    answer = llm_unhandled_answer(question, bedrock_client, kwargs) if 'NoSuchKey' in answer else answer

    return {
        'statusCode': 200,
        'body': json.dumps({'results': answer,
                            'system_prompt': get_summary_history
                            }),
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},

    }
