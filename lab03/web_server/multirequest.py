#!/usr/bin/python
import os
from threading import *

commands = ['python3 socket_client_3.py localhost 1337 aboba.txt', 
            'python3 socket_client_3.py localhost 1337 aboba.py', 
            'python3 socket_client_3.py localhost 1337 folder/bebra.py', 
            'python3 socket_client_3.py localhost 1337 test.png', 
            'python3 socket_client_3.py localhost 1337 bebra.txt',
            ]

def make_request(i):
    os.system('/bin/bash -c \"' + commands[i] + '\"') 


for i in range(5):
    thread = Thread(target=make_request, args=(i,))
    thread.start()