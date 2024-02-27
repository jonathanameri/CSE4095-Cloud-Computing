import json

def lambda_handler(event, context):
    bucket_name = event["bucket"]
    print('bucket_name:', bucket_name)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
