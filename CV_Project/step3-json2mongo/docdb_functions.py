import json
import boto3
import pymongo
import ssl
from s3_functions import get_docdb_pem


def get_docdb_cred(pem_path):
    '''
    connects to the docdb
    '''
    
    client = pymongo.MongoClient(
    "mongodb://developer:developer@docdb-cv.cocluqwjpuyf.us-east-1.docdb.amazonaws.com:27017/?ssl=true&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false",
    serverSelectionTimeoutMS=10000,
    tls=True,
    tlsCAFile=pem_path,
    tlsAllowInvalidHostnames=False
)
    
    return client


def import_to_docdb(s3_client, s3_kwargs, docdb_client, obj_list):
    '''
    imports the json files into docDB
    '''
    
    db = docdb_client['db-cv']
    collection = db['cv-collection']
    
    for obj in obj_list:
        
        if obj.endswith('.json'):
            response = s3_client.get_object(Bucket = s3_kwargs['bucket'], Key = obj)
            obj_body = response['Body'].read().decode('utf-8')
            
            json_data = json.loads(obj_body)
            
            if isinstance(json_data, list):
                result = collection.insert_many(json_data)
                print(f"Inserted {len(result.inserted_ids)} documents from {obj}")
            elif isinstance(json_data, dict):
                result = collection.insert_one(json_data)
                print(f"Inserted {len(result.inserted_ids)} documents from {obj}")