import json
import boto3
from pymongo import MongoClient
from s3_functions import get_docdb_pem
import os


def import_to_docdb(s3_client, s3_kwargs, obj_list):
    '''
    imports the json files into docDB
    '''
    client = MongoClient(host=os.environ.get('URI'))

    db = client.candidates
    collection = db.candidates_cv

    for obj in obj_list:

        if obj.endswith('.json'):
            response = s3_client.get_object(Bucket=s3_kwargs['bucket'], Key=obj)
            obj_body = response['Body'].read()

            json_data = json.loads(obj_body)

            # upserts the data based on phoneNumber
            if isinstance(json_data, dict):
                result = collection.update_one(
                    {"email": json_data.get("email")},
                    {"$set": json_data},
                    upsert=True
                )
                if result.matched_count > 0:
                    print(f'Successfully upserted {json_data.get("candidateName")}')
                else:
                    print(f'failed upserting {json_data.get("candidateName")}')

