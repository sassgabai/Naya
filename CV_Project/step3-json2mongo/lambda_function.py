import json
from s3_functions import generate_s3_client, get_s3_objects, get_docdb_pem
from docdb_functions import import_to_docdb

import os


def lambda_handler(event, context):
    # configure s3 client and kwargs
    s3_client, s3_kwargs = generate_s3_client()

    # get a list of json objects
    obj_list = get_s3_objects(s3_client, s3_kwargs)

    # import the json files to COMPASS
    import_to_docdb(s3_client, s3_kwargs, obj_list)

    return {
        'statusCode': 200,
        'body': json.dumps(f'sucessfully upserted {len(obj_list)} objects.')
    }
