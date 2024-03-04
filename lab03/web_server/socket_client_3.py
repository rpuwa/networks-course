# sample cmd to run: python3 socket_client_3.py localhost 1337 aboba.txt
from socket import *
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('host')
parser.add_argument('port')
parser.add_argument('file')
args = parser.parse_args()
server_name = args.host
server_port = int(args.port)
filename = args.file

sock = socket(AF_INET, SOCK_STREAM)
sock.connect((server_name, server_port))
sock.sendall(str.encode(f'GET /{filename} HTTP/1.1\n'))
filedata = sock.recv(2 ** 16)
try:
    print(filedata.decode())
except:
    print('Not a text file')
sock.close()
