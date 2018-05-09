import socket
import json
from pprint import pprint


def send_tasks(conn):
    with open('elo.json') as datafile:
        data = datafile.read()
        conn.send(data.encode())



def add_task(my_socket,conn):
    with open('elo.json') as datafile:
        data = json.load(datafile)
    print(data)

    tasks = data['tasks']
    last_index = data['last_index']
    task = {}
    task['id'] = last_index + 1
    task['description'] = conn.recv(1024).decode()
    task['priority'] = conn.recv(1024).decode()

    tasks.append(task)

    data['last_index'] = last_index + 1
    data['tasks'] = tasks
    with open('elo.json', 'w') as outfile:
        json.dump(data, outfile, sort_keys=True, indent=4,ensure_ascii=False)




def delete_task(conn):
    del_id = conn.recv(1024).decode()
    with open('elo.json') as datafile:
        data = json.load(datafile)
    last_index = data['last_index']
    new_tasks = {'last_index': last_index, 'tasks': []}
    for t in data['tasks']:
      if t['id'] != int(del_id):
          new_tasks['tasks'].append(t)

    with open('elo.json', 'w') as outfile:
        json.dump(new_tasks, outfile, sort_keys=True, indent=4,ensure_ascii=False)



def priority_task(conn):
    priority = conn.recv(1024).decode()
    with open('elo.json') as datafile:
        data = json.load(datafile)

    tasks_to_send = {'tasks': []}

    for t in data['tasks']:
        if t['priority'] == priority:
            tasks_to_send['tasks'].append(t)
    temp = str(tasks_to_send)
    conn.send(temp.encode())


def main():

     host = "127.0.0.1"
     port = 5000
     my_socket = socket.socket()
     my_socket.bind((host, port))
     my_socket.listen(5)
     conn, addr = my_socket.accept()
     print("Connection from: " + str(addr))
     while 1:
         request = conn.recv(1024).decode()
         if request == '1':
             send_tasks(conn)
         elif request == '2':
             add_task(my_socket,conn)
         elif request == '3':
             delete_task(conn)
         elif request == '4':
             priority_task(conn)
         elif request == '5':
             exit()


if __name__ == '__main__':
    main()
