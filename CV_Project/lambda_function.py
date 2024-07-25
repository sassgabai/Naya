import json
import boto3
from s3_functions import generate_s3_client, get_s3_objects, get_obj_body, write_to_s3
from bedrock_functions import generate_bedrock_client, activate_prompt, send_to_llm


def lambda_handler(event, context):
    # generate clients
    s3_client, s3_kwargs = generate_s3_client()
    bedrock_client, bedrock_kwargs = generate_bedrock_client()

    obj_list = get_s3_objects(s3_client, s3_kwargs)

    for obj in obj_list:
        # get body
        obj_body = get_obj_body(obj, s3_client, s3_kwargs)

        # send to prompt
        answer = send_to_llm(obj_body, bedrock_client, bedrock_kwargs)

        write_to_s3(answer, obj, s3_client, s3_kwargs)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
