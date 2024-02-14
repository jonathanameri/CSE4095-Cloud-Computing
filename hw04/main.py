"""
Python application to interact with AWS S3. Includes a number of functions.
The application interacts with the AWS account that is specified in the '~/.aws/credentials' file.
"""
import os
import boto3
from botocore.exceptions import ClientError

def main_menu():
    """
    This function displays the main menu of the application in a loop.
    It provides the following options to the user:
    - 'list_buckets': List all buckets and allows the user to select one.
    - 'backup': Backup files from a local folder.
    - 'list_objects': List all objects in the selected bucket.
    - 'download': Download a specific object from the selected bucket.
    """
    selected_bucket = None
    while True:
        # Display the main menu
        print('***** Main Menu *****\n')
        print('select an option by typing the command name')
        print('\t- \'list_buckets\': List all buckets and select one')
        print('\t- \'upload\': Upload files from local folder')
        print('\t- \'list_contents\': List all objects in selected bucket')
        print('\t- \'get_file\': Download a specific object from selected bucket')
        print('\t- \'exit\': Exit the application')

        # Define valid commands
        valid_commands = ['list_buckets', 'upload', 'list_contents', 'get_file', 'exit']

        # Get user input
        command = input('\nEnter a command: ')

        # Process user input
        if command not in valid_commands:
            print('\n!!!!!!!!!! Invalid command !!!!!!!!!!\n')
        elif command == 'list_buckets':
            selected_bucket = list_buckets()
        elif command == 'exit':
            break
        elif selected_bucket is None:
            print('\nYou must select a bucket first\n')
        elif command == 'upload':
            local_folder_name = input('Specify the local folder name: ')
            upload(selected_bucket, local_folder_name)
        elif command == 'list_contents':
            folder = input('Specify the folder name (leave blank to see all resources): ')
            list_contents(selected_bucket, folder)
        elif command == 'get_file':
            object_name = input('Specify the object name: ')
            file_name = input('Specify the file name: ')
            get_file(selected_bucket, object_name, file_name)
        else:
            print('\n!!!!!!!!!! Invalid command !!!!!!!!!!\n')

def list_buckets():
    """
    This function lists all buckets and allows the user to select one.
    """
    s3 = boto3.resource('s3')

    list_of_buckets = []
    bucket_name = None

    print('\nList of buckets:')
    for bucket in s3.buckets.all():
        list_of_buckets.append(bucket.name)
        print(bucket.name)
    while list_of_buckets:
        bucket_name = input('\nEnter the name of the bucket you want to select: ')
        if bucket_name in list_of_buckets:
            break
        print('Invalid bucket name')
    print()
    return bucket_name

def upload(bucket_name, local_folder_name):
    """
    This function uploads files from a local folder to the selected bucket.
    Iterates over all files in the local folder and uploads them to the selected bucket.

    Files are uploaded one at a time
    """
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)

    print('\nUploading files to S3...\n')

    if os.path.isdir(local_folder_name):
        for filename in os.listdir(local_folder_name):
            file_path = os.path.join(local_folder_name, filename)
            if os.path.isfile(file_path):
                bucket_file = filename  # Upload to S3 with the same filename
                print(f'Uploading {filename} to {bucket_name}/{bucket_file}')
                bucket.upload_file(file_path, bucket_file)
            else:
                print(f'Skipping directory: {filename}')
        print('\nFiles uploaded successfully')
    else:
        print(f"\nError: The directory {local_folder_name} does not exist.")
    print()

def list_contents(bucket_name, server_folder_name):
    """
    This function lists all objects in the selected folder.
    """
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    print(f'\nListing contents of folder \'/{server_folder_name}\' in bucket \'{bucket_name}\':\n')
    if server_folder_name:
        for bucket_object in bucket.objects.filter(Prefix=server_folder_name):
            print(bucket_object.key)
    else:
        for bucket_object in bucket.objects.all():
            print(bucket_object.key)
    print()

def get_file(bucket_name, object_name, file_name):
    """
    This function downloads a specific object from the selected bucket.
    The parameters are:
    - bucket_name: the name of the bucket
    - object_name: the name of the object
    - file_name: the name of the file to download
    """
    s3 = boto3.client('s3')
    print('\nDownloading file...\n')
    try:
        s3.download_file(bucket_name, object_name, file_name)
    except ClientError as e:
        print(e)

if __name__ == '__main__':
    main_menu()
