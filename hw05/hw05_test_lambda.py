'''
Tests for lambda function defined in ./lambda1/lambda_python.py
'''
import time
import boto3
from botocore.exceptions import ClientError

# Constants
BUCKET_NAME = 'hw05-jonathan-ameri'
DYNAMODB_TABLE_NAME = 'hw05-table'
FILE_NAME = 'test.txt'

# Create s3 client
s3 = boto3.client('s3')

# Create dynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(DYNAMODB_TABLE_NAME)

def permanently_delete_object(bucket, object_key):
    """
    Permanently deletes a versioned object by deleting all of its versions.

    Usage is shown in the usage_demo_single_object function at the end of this module.

    :param bucket: The bucket that contains the object.
    :param object_key: The object to delete.
    """
    s3resource = boto3.resource('s3')
    bucket = s3resource.Bucket(bucket)
    try:
        bucket.object_versions.filter(Prefix=object_key).delete()
        print(f"Permanently deleted all versions of object {object_key}.")
    except ClientError:
        print(f"Couldn't delete all versions of {object_key}.")
        raise

def delete_dynamodb_record(filename):
    '''
    Function to delete record from dynamoDB
    '''
    table.delete_item(Key={'filename': filename})

def upload_file_to_s3(filename, content):
    '''
    Function to upload file to s3
    '''
    s3.put_object(Bucket=BUCKET_NAME, Key=filename, Body=content)

def get_dynamodb_record(filename):
    '''
    Function to fetch record from dynamoDB
    '''
    response = table.get_item(Key={'filename': filename})
    print('response:', response)
    if 'Item' in response:
        return response['Item']
    print(f'File {filename} not found in dynamoDB')
    return None

def test_s3_file_not_exist():
    '''
    Test if the test file is not in s3
    '''
    # Delete all versions of the file and erase the record from dynamoDB
    permanently_delete_object(BUCKET_NAME, FILE_NAME)
    delete_dynamodb_record(FILE_NAME)

    time.sleep(15)
    record = get_dynamodb_record(FILE_NAME)
    assert record is None

def test_s3_upload_and_update():
    '''
    Test file upload in s3 and check if record is created in dynamoDB
    Also update the file and check if record is updated in dynamoDB
    '''

    # Upload file to s3
    upload_file_to_s3(FILE_NAME, 'test content')
    time.sleep(15)

    # Check if file is in s3
    record = get_dynamodb_record(FILE_NAME)
    assert record is not None
    assert record['filename'] == FILE_NAME
    assert record['bucketARN'] is not None
    assert record['eTag'] is not None
    assert record['fileSize'] is not None
    assert record['uploadTime'] is not None

    pre_upload_time = record['uploadTime']

    # Update file in s3
    upload_file_to_s3(FILE_NAME, 'new test content')
    time.sleep(15)
    # Check if file is in s3
    record = get_dynamodb_record(FILE_NAME)
    assert record is not None
    assert record['filename'] == FILE_NAME
    assert record['uploadTime'] != pre_upload_time
