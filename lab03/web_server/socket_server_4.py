# sample cmd to run: python3 socket_server_2.py 1337
from socket import *
from threading import *
import os
from argparse import ArgumentParser

def make_responce(client_sock, addr, sem):
    try:
        filename = client_sock.recv(2 ** 16).decode().split()[1][1:]
        filepath = os.path.join(os.getcwd(), filename)
        print(f'{addr[1]}: Request to read {filename} file')
        with open(filepath, 'rb') as file:
            filedata = file.read()
            client_sock.sendall(str.encode('HTTP/1.1 200 OK\n\n') + filedata)
        print(f'{addr[1]}: OK!')
    except FileNotFoundError:
        client_sock.sendall(str.encode('HTTP/1.1 404 Not Found\n\n'))
        print(f'{addr[1]}: File Not Found')
    except IndexError:
        client_sock.sendall(str.encode('HTTP/1.1 400 Bad Request\n\n'))
        print(f'{addr[1]}: Bad Request')
    except:
        client_sock.sendall(str.encode('HTTP/1.1 418 I\'m a teapot\n\n'))
        print(f'{addr[1]}: Other error occurred')
    client_sock.close()
    sem.release()
    print(f'{addr[1]}: End operation')

parser = ArgumentParser()
parser.add_argument('port')
parser.add_argument('concurrency_level')
args = parser.parse_args()
server_port = int(args.port)
server_concurrency = int(args.concurrency_level)

server_sock = socket(AF_INET, SOCK_STREAM)
server_sock.bind(('', server_port))
server_sock.listen(228)
sem = Semaphore(server_concurrency)
print(f'The server is listening on port {server_port}...')

while True:
    client_sock, addr = server_sock.accept()
    sem.acquire()
    print(f'{addr[1]}: Begin operation')
    thread = Thread(target=make_responce, args=(client_sock, addr, sem))
    thread.start()
