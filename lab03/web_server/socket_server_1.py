# sample cmd to run: python3 socket_server_1.py 1337
from socket import *
import os
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('port')
args = parser.parse_args()
server_port = int(args.port)

server_sock = socket(AF_INET, SOCK_STREAM)
server_sock.bind(('', server_port))
server_sock.listen(1)
print(f'The server is listening on port {server_port}...')
while True:
    client_sock, addr = server_sock.accept()
    try:
        filename = client_sock.recv(2 ** 16).decode().split()[1][1:]
        print(f'{addr[1]}: Request to read {filename} file')
        filepath = os.path.join(os.getcwd(), filename)
        with open(filepath, 'rb') as file:
            filedata = file.read()
            client_sock.sendall(str.encode('HTTP/1.1 200 OK\n\n') + filedata)
        print('OK!')
    except FileNotFoundError:
        client_sock.sendall(str.encode('HTTP/1.1 404 Not Found\n\n'))
        print('File Not Found')
    except IndexError:
        client_sock.sendall(str.encode('HTTP/1.1 400 Bad Request\n\n'))
        print(f'{addr[1]}: Bad Request')
    except:
        client_sock.sendall(str.encode('HTTP/1.1 418 I\'m a teapot\n\n'))
        print('Other error occurred')
    client_sock.close()
