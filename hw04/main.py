"""
Python application to interact with AWS S3. Includes a number of functions.
The application interacts with the AWS account that is specified in the '~/.aws/credentials' file.
"""
import boto3

s3 = boto3.resource('s3')
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
        print('\t- \'backup\': Backup files from local folder')
        print('\t- \'list_contents\': List all objects in selected bucket')
        print('\t- \'get_file\': Download a specific object from selected bucket')
        print('\t- \'exit\': Exit the application')

        # Define valid commands
        valid_commands = ['list_buckets', 'backup', 'list_contents', 'get_file', 'exit']

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
            print('You must select a bucket first')
        elif command == 'backup':
            upload(selected_bucket)
        elif command == 'list_contents':
            folder = input('Specify the folder name: ')
            list_contents(selected_bucket, folder)
        elif command == 'download':
            get_file(selected_bucket)
        else:
            print('\n!!!!!!!!!! Invalid command !!!!!!!!!!\n')

def list_buckets():
    """
    This function lists all buckets and allows the user to select one.
    """
    list_of_buckets = []
    bucket_name = None

    print('\nList of buckets:')
    for bucket in s3.buckets.all():
        list_of_buckets.append(bucket.name)
        print(bucket.name)
    while True and list_of_buckets:
        bucket_name = input('\nEnter the name of the bucket you want to select: ')
        if bucket_name in list_of_buckets:
            break
        else:
            print('Invalid bucket name')
    print()
    return bucket_name

def upload(localFolderName, bucketName):
    """
    This function uploads files from a local folder to the selected bucket.
    """
    print('Backing up files...')


def list_contents(bucketName, serverFolderName):
    """
    This function lists all objects in the selected bucket.
    """
    bucket = s3.Bucket(bucketName)
    print('\nListing contents of the selected bucket:')
    for bucket_object in bucket.objects.all():
        print(bucket_object.key)
    print()

def get_file(bucketName, serverFolderName, fileName):
    """
    This function downloads a specific object from the selected bucket.
    """
    print('Downloading a specific object...')

if __name__ == '__main__':
    main_menu()
