import json
from s3_functions import generate_s3_client, get_s3_objects, get_docdb_pem
from docdb_functions import get_docdb_cred, import_to_docdb
import pymongo

def lambda_handler(event, context):
    
    #configure s3 client and kwargs
    s3_client, s3_kwargs = generate_s3_client()
    
    #get a list of json objects
    obj_list = get_s3_objects(s3_client, s3_kwargs)
    
    #generate the docdb pem into lambda tmp
    pem_path = get_docdb_pem(s3_client, s3_kwargs)
    
    #connect to docdb
    docdb_client = get_docdb_cred(pem_path)
    
    #import the json files to docdb
    import_to_docdb(s3_client, s3_kwargs, docdb_client, obj_list)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
