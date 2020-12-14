import json
import boto3
import os
import requests
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth


host = '' # For example, my-test-domain.us-east-1.es.amazonaws.com
region = '' # e.g. us-west-1

service = 'es'
credentials = boto3.Session().get_credentials()
access_key = credentials.access_key
secret_key = credentials.secret_key
awsauth = AWS4Auth(access_key, secret_key, region, service, session_token = credentials.token)

def lambda_handler(event,context):
    # os.environ['TZ'] = 'America/New_York'
    # time.tzset()
    client = boto3.client('lex-runtime')
    response_lex = client.post_text(
        botName='SearchPhotos',
        botAlias="photoBot",
        userId="user",
        inputText= event["queryStringParameters"]['q']
    )
    print("this is inputText: ", event["queryStringParameters"]['q'])
    print("this is Lex response: ", response_lex)
    try:
        queryOne = response_lex['slots']['slotOne']
        print("this is query one: ", queryOne)
        es = Elasticsearch(
            hosts = [{'host': host, 'port': 443}],
            http_auth = awsauth,
            use_ssl = True,
            verify_certs = True,
            connection_class = RequestsHttpConnection
        )
        search_body = {
            "query": {
                "match": {
                    "labels": queryOne
                }
            }
        }
        # es.indices.delete(index='photos', ignore=[400, 404])
        res = es.search(index="photos", body = search_body)
        print("this is Elastic Search: ", res)
        result = set()
        for hit in res['hits']['hits']:
            result.add(hit["_source"]["objectKey"])
        if(response_lex['slots']['slotTwo'] != None):
            queryTwo = response_lex['slots']['slotTwo']
            search_body = {
                "query": {
                    "match": {
                        "labels": queryTwo
                    }
                }
            }
            res = es.search(index="photos", body = search_body)
            for hit in res['hits']['hits']:
                result.add(hit["_source"]["objectKey"])
    except:
        result = set()
    resultList = []
    for element in result:
        resultList.append(element)
    if len(resultList) == 0:
        resultList.append("ImageNotAvailable.jpg")
    print("this is resultList: ", resultList)
    return {
        'headers': {"Access-Control-Allow-Origin" : "*",
                    "Access-Control-Allow-Credentials": True
        },
        'statusCode': 200,
        'body': json.dumps(resultList)
    }