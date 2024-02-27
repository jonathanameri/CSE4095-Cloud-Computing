import json
import boto3

def lambda_handler(event, context):

    print('list_buckets. event:', event)

    s3 = boto3.client('s3')
    response = s3.list_buckets()

    bucket_list = []
    for bucket in response['Buckets']:
        bucket_list.append(bucket['Name'])

    return {
        'statusCode': 200,
        'body': json.dumps(bucket_list)
    }
