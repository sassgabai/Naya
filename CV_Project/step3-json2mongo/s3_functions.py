import json
import boto3


def generate_s3_client():
    s3_client = boto3.client('s3')

    kwargs = {
        'bucket': 'sassi-cv',
        'src_prefix': 'json/'
    }

    return s3_client, kwargs


def get_s3_objects(s3_client, kwargs) -> list:
    '''
    Gets all obj in txt/ folder into a list
    '''
    objects = s3_client.list_objects_v2(Bucket=kwargs['bucket'], Prefix=kwargs['src_prefix'])

    # get all obj in bucket to a list
    obj_list = [obj['Key'] for obj in objects['Contents']]
    # obj_list = [obj.replace('txt/', '') for obj in obj_list]

    return obj_list


def get_docdb_pem(s3_client, kwargs) -> str:
    '''
    get the cert.pem file in s3 and store in /tmp folder in the lambda_handler, and returns the tmp path
    '''
    bucket_name = kwargs['bucket']
    key = 'global-bundle.pem'

    local_tmp_path = '/tmp/global-bundle.pem'

    s3_client.download_file(bucket_name, f"zipped/{key}", local_tmp_path)

    return local_tmp_path
