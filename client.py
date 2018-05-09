import socket
import json

def print_priority_task(mySocket):
    mySocket.send(input("Podaj priorytet: ").encode())
    data = mySocket.recv(1024).decode()
    print(data)


def print_task(mySocket):
    data = mySocket.recv(1024).decode()
    tasks = json.loads(data)
    print(tasks)
    for t in tasks['tasks']:
        print('ID: ' + str(t['id']) + ', Opis: ' + t['description'] + ', Priorytet: ' + str(t['priority']))

def main():
    host = '127.0.0.1'
    port = 5000
    mySocket = socket.socket()
    mySocket.connect((host, port))
    while 1:
        print("1 - Wyświetl zadanie")
        print("2 - Dodaj zadanie")
        print("3 - Usuń zadanie")
        print("4 - Wyświetl zadania z danym priorytetem")
        print("5 - Wyjście")

        choice = input('Wybierz: ')
        mySocket.send(choice.encode())

        if choice == '1':
            print_task(mySocket)
        elif choice == '2':
            mySocket.send(input("Opis: ").encode())
            mySocket.send(input("Priorytet: ").encode())
        elif choice == '3':
            mySocket.send(input("ID do usunięcia: ").encode())
        elif choice == '4':
            #mySocket.send(input("Podaj priorytet: ").encode())
            print_priority_task(mySocket)
        elif choice == '5':
            mySocket.send('5'.encode())
            mySocket.close()
            exit()




if __name__ == '__main__':
    main()
