import json
import boto3
import elasticsearch
from requests_aws4auth import AWS4Auth
import requests

def lambda_handler(event, context):
    # TODO implement
    region = "us-east-1"
    service = 'es'
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Changed Zip!')
    }
