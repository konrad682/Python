import json, os
import paramiko


def overwrite(RemoteFolder,JsonFile,SFTP,LocalFolder):
    for file in LocalFolder:
        if file.split('.')[-1] not in JsonFile['ignore']:
           SFTP.put(JsonFile['local_folder'] + '/' + file, JsonFile['remote_folder'] + '/' + file)
        print(file)

def uptade(LoaclFolder, RemoteFolder,JsonFile,SFTP,RemotePath, LocalPath):
    for file in LoaclFolder:
        if file in RemoteFolder:
           # print(SFTP.stat(RemotePath + "/" + file).st_mtime)
           # print(os.path.getctime(LocalPath + "/" + file))
            if SFTP.stat(RemotePath+"/"+file).st_mtime < os.path.getmtime(LocalPath+"/"+file):

                #print(SFTP.stat(RemotePath+"/"+file).st_mtime)
                #print(os.path.getctime(LocalPath+"/"+file))

                if file.split('.')[-1] not in JsonFile['ignore']:
                    print(file)
                    SFTP.put(JsonFile['local_folder'] + '/' + file, JsonFile['remote_folder'] + '/' + file)


def add_not_existing(LoaclFolder, RemoteFolder,JsonFile,SFTP):
    for file in LoaclFolder:
        if file not in RemoteFolder:
            if file.split('.')[-1] not in JsonFile['ignore']:
                print(file)
                SFTP.put(JsonFile['local_folder'] + '/' + file, JsonFile['remote_folder'] + '/' + file)


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
        overwrite(RemoteFolder,JsonFile,SFTP,LocalFolder)
    elif choice == '2':
        uptade(LocalFolder,RemoteFolder,JsonFile,SFTP,RemotePath,LocalPath)
    elif  choice == '3':
        add_not_existing(LocalFolder,RemoteFolder,JsonFile,SFTP)
    else:
        print("Dont choose anything option")

    SFTP.close()
    client.close()

if __name__ == '__main__':
    main()