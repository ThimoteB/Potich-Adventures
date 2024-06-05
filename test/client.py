# coding: utf-8

import socket
from time import sleep

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("", 44440))

print("Connecté")

# message = b"Hello, client"
# s.send(message)
# print("sent:", message)

while True:
    data = s.recv(1024)
    print(data)
    sleep(1)

sleep(10)

s.close()

print("Disconnected")

# End of file