import json
import boto3

def lambda_handler(event, context):
    bucket_name = event["bucket"]

    print('bucket_name:', bucket_name)
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=bucket_name)

    print('response:', response)

    object_list = []
    for obj in response['Contents']:
        object_list.append(obj['Key'])
    
    return {
        'statusCode': 200,
        'body': json.dumps(object_list)
    }
