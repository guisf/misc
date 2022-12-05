#!/usr/bin/env python

import socket

if __name__ == '__main__':
    address = ('', 50000)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(address)
    a = raw_input('> ')
    client.sendall(a + '\n')
    print client.recv(1024)
    client.close()

