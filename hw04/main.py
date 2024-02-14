def main_menu():
    """
    This function displays the main menu of the application in a loop.
    It provides the following options to the user:
    - 'list_buckets': List all buckets and allows the user to select one.
    - 'backup': Backup files from a local folder.
    - 'list_objects': List all objects in the selected bucket.
    - 'download': Download a specific object from the selected bucket.
    """
    while True:
        print('select an option by typing the command name')
        print('\'list_buckets\': List all buckets and select one')
        print('\'backup\': Backup files from local folder')
        print('\'list_objects\': List all objects in selected bucket')
        print('\'download\': Download a specific object from selected bucket')
        print('\'exit\': Exit the application')

        command = input('Enter a command: ')
        if command == 'list_buckets':
            list_buckets()
        elif command == 'backup':
            backup()
        elif command == 'list_objects':
            list_objects()
        elif command == 'download':
            download()
        elif command == 'exit':
            break
        else:
            print('Invalid command')

def list_buckets():
    """
    This function lists all buckets and allows the user to select one.
    """
    print('Listing all buckets...')

def backup():
    """
    This function backs up files from a local folder to a selected bucket.
    """
    print('Backing up files...')


def list_objects():
    """
    This function lists all objects in the selected bucket.
    """
    print('Listing all objects...')

def download():
    """
    This function downloads a specific object from the selected bucket.
    """
    print('Downloading a specific object...')

if __name__ == '__main__':
    main_menu()
