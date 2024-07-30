import boto3
import json
from claude import claude_system_prompt, claude_answer, claude_unhandled_prompt, claude_summarize


def llm_answer(question, page_number, bedrock_client, kwargs):
    '''
    Returns the final answer to the client
    '''

    s3_client = boto3.client('s3')

    bucket = 'genaya-backend'
    sub_dir = 'raw_files/'
    try:
        txt_file = s3_client.get_object(Bucket=bucket, Key=f"{sub_dir}{page_number}.txt")

    except Exception as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            return 'NoSuchKey'

    txt_data = txt_file['Body'].read().decode('utf-8')

    txt_body = txt_data.split('content:')[1].split('url:')[0]

    txt_url = txt_data.split('url:')[1]

    body = claude_answer(question, txt_body, txt_url)

    kwargs['body'] = json.dumps(body)

    response = bedrock_client.invoke_model(**kwargs)

    response_json = json.loads(response.get("body").read())
    output = response_json.get("content", [])
    full_response = ""

    for obj in output:
        full_response += obj["text"]

    return full_response


def llm_unhandled_answer(question, bedrock_client, kwargs):
    '''
    Returns the failure answer to the client
    '''

    body = claude_unhandled_prompt(question)

    kwargs['body'] = json.dumps(body)

    response = bedrock_client.invoke_model(**kwargs)

    response_json = json.loads(response.get("body").read())
    output = response_json.get("content", [])
    full_response = ""

    for obj in output:
        full_response += obj["text"]

    return full_response


def llm_summarize(question, history_list, get_system_prompt, bedrock_client, kwargs):
    body = claude_summarize(question, history_list, get_system_prompt)

    kwargs['body'] = json.dumps(body)

    response = bedrock_client.invoke_model(**kwargs)

    response_json = json.loads(response.get("body").read())
    output = response_json.get("content", [])
    full_response = ""

    for obj in output:
        full_response += obj["text"]

    return full_response


def llm_system_result(question, bedrock_client, kwargs):
    '''
    returns the answer from the system_prompt to the lambda
    '''
    prompt_body = claude_system_prompt(question)

    kwargs['body'] = json.dumps(prompt_body)

    response = bedrock_client.invoke_model(**kwargs)

    response_json = json.loads(response.get("body").read())
    output = response_json.get("content", [])
    full_response = ""

    for obj in output:
        full_response += obj["text"]

    return full_response