import json, os
import paramiko


def overwrite(RemoteFolder,JsonFile,SFTP):
    for file in RemoteFolder:
        if file.split('.')[-1] not in JsonFile['ignore']:
           SFTP.get(JsonFile['remote_folder'] + '/' + file, JsonFile['local_folder'] + '/' + file)
        print(file)

def uptade(LoaclFolder, RemoteFolder,JsonFile,SFTP):
    for file in RemoteFolder:
        if file in LoaclFolder:
            if file.split('.')[-1] not in JsonFile['ignore']:
                print(file)
                SFTP.get(JsonFile['remote_folder'] + '/' + file, JsonFile['local_folder'] + '/' + file)


def add_not_existing(LoaclFolder, RemoteFolder,JsonFile,SFTP):
    for file in RemoteFolder:
        if file not in LoaclFolder:
            if file.split('.')[-1] not in JsonFile['ignore']:
                print(file)
                SFTP.get(JsonFile['remote_folder'] + '/' + file, JsonFile['local_folder'] + '/' + file)










def main():
    client = paramiko.SSHClient()
    client.load_system_host_keys(filename=None)
    ssh_stdin = ssh_stdout = ssh_stderr = None
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy)

    with open('konfiguracja.json') as datafile:
        JsonFile = json.loads(datafile.read())
        SSH_HOST = JsonFile['server_addres']
        SSH_PORT = JsonFile['port']
        SSH_USERNAME = JsonFile['username']
        SSH_PASSWORD =  input("Password: ")

    try:
        client.connect(SSH_HOST,SSH_PORT,SSH_USERNAME,SSH_PASSWORD)
    except paramiko.AuthenticationException:
        print("Wrong password !")
        client.close()

    SFTP = client.open_sftp()

    #shh = paramiko.sftp_client.SFTP

    RemotePath = JsonFile["remote_folder"]
    LocalPath = JsonFile["local_folder"]

    try:
        os.stat(LocalPath)
    except OSError:
        os.mkdir(LocalPath)

    LocalFolder = os.listdir(LocalPath)
    RemoteFolder = SFTP.listdir(RemotePath)
    print(RemoteFolder)

    print("1 - overwrite\n2- uptade\n3- add_not_existing")

    choice = input("Option: ")
    if choice == '1':
        overwrite(RemoteFolder,JsonFile,SFTP)
    elif choice == '2':
        uptade(LocalFolder,RemoteFolder,JsonFile,SFTP)
    elif  choice == '3':
        add_not_existing(LocalFolder,RemoteFolder,JsonFile,SFTP)
    else:
        print("Dont choose anything option")

    SFTP.close()
    client.close()

if __name__ == '__main__':
    main()