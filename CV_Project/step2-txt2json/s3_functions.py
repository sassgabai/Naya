import json
import boto3


def generate_s3_client():
    
    s3_client = boto3.client('s3')
    
    kwargs ={
        'bucket': 'sassi-cv',
        'src_prefix': 'txt/',
        'des_prefix': 'json/'
    }
    
    return s3_client, kwargs
    
    
def get_s3_objects(s3_client, kwargs) ->list:
    '''
    Gets all obj in txt/ folder into a list
    '''
    objects = s3_client.list_objects_v2(Bucket=kwargs['bucket'], Prefix=kwargs['src_prefix'])
    
    # get all obj in bucket to a list 
    obj_list = [obj['Key'] for obj in objects['Contents']]
    obj_list = [obj.replace('txt/', '') for obj in obj_list]
       
    return obj_list
    
def get_obj_body(obj, s3_client, s3_kwargs) ->str:
    '''
    Gets obj name and returns the content of the obj
    '''
    
    response = s3_client.get_object(Bucket=s3_kwargs['bucket'], Key= f"{s3_kwargs['src_prefix']}{obj}")
    content = response['Body'].read().decode('utf-8')
    
    return content
    
    
def write_to_s3(answer, obj, s3_client, kwargs):
    '''
    write the llm answer into s3 inside json/
    '''
    key = f"{kwargs['des_prefix']}{obj.replace('.txt','.json')}"
    
    s3_client.put_object(Bucket= kwargs['bucket'], Body= answer, Key= key)