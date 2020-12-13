from requests_aws4auth import AWS4Auth
import json
import boto3
from elasticsearch import Elasticsearch, RequestsHttpConnection

def lambda_handler(event, context):
    #Get S3 name and object name
    bucket_name = event["Records"][0]['s3']['bucket']['name']
    object_key = event["Records"][0]['s3']['object']['key']
    event_time = event["Records"][0]["eventTime"]
    print(f"{bucket_name} / {object_key}")

    #Rekogition process image
    rekogition_client =boto3.client('rekognition')
    reko_response = rekogition_client.detect_labels(
        Image={
            'S3Object':{'Bucket':bucket_name,'Name':object_key}
            },
        MaxLabels=10,
        MinConfidence = 75)
    reko_lables = []
    for label in reko_response['Labels']:
        reko_lables.append(label['Name'])
    print(reko_lables)

    #Elastic Search index data
    host = "vpc-photo-album-es-6tsvd6fttfhzjkrmo4hpfonwei.us-east-1.es.amazonaws.com"
    path = "photos"
    region = "us-east-1"

    service = 'es'
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
    es = Elasticsearch(
        hosts = [{'host': host, 'port': 443}],
        http_auth = awsauth,
        use_ssl = True,
        verify_certs = True,
        connection_class = RequestsHttpConnection
    )
    # The JSON body to accompany the request (if necessary)
    payload = {
        "objectKey": object_key,
        "bucket": bucket_name,
        "createdTimestamp":event_time,
        "labels":reko_lables
    }
    res = es.index(index=path, doc_type="_doc", body=payload)
    print(res)

    return {
        'statusCode': 200,
        'body': json.dumps("Hello World")
    }
