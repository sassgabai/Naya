import boto3
from botocore.exceptions import ClientError
import json

def get_secret():
    
        secret_name = "rds!cluster-3f87466e-e02e-4d13-8a81-8ee1b07cb6af"
        region_name = "us-east-1"
    
        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )
    
        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            raise e
    
        return json.loads(get_secret_value_response['SecretString'])