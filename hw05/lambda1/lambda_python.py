import json
import boto3

def lambda_handler(event, context):
    # Extract all the metadata from event
    s3 = event['Records'][0]['s3']
    object = s3['object']
    
    # Data for DynamoDB record
    filename = object['key']
    fileSize = object['size']
    uploadTime = event['Records'][0]['eventTime']
    bucketARN = s3['bucket']['arn']
    eTag = object['eTag']
    
    # Convert fileSize to string
    fileSizeStr = str(fileSize)
    
    # Log to CloudWatch
    record={
        'filename':{'S':filename},
        'fileSize':{'N':fileSizeStr},
        'uploadTime':{'S':uploadTime},
        'bucketARN':{'S':bucketARN},
        'eTag':{'S':eTag}
    }
    print('record:', record)
    
    # Create dynamodb client
    dynamodb = boto3.client('dynamodb')
    
    # Check if item exists already
    response = dynamodb.get_item(TableName='hw05-table', Key={'filename':{'S':filename}})
    
    print('response from get_item:', response)
    
    if not 'Item' in response:
        print('item does not already exist in the table, putting item in DynamoDB table')
        dynamodb.put_item(TableName='hw05-table', Item=record)
    else:
        print('item already exists in the table, updating item in DynamoDB table')
        dynamodb.update_item(
            TableName='hw05-table',
            Key={'filename':{'S':filename}},
            UpdateExpression='SET fileSize = :size, uploadTime = :upload, bucketARN = :arn, eTag = :tag',
            ExpressionAttributeValues={
                ':size': {'N': fileSizeStr},
                ':upload': {'S': uploadTime},
                ':arn': {'S': bucketARN},
                ':tag': {'S': eTag}
            }
        )
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
