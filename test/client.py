# coding: utf-8

import socket
from time import sleep

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("", 44440))

print("Connecté")

message = s.recv(1024)
message = message.decode()
print('recv:', message)

print("5")
sleep(1)
print("4")
sleep(1)
print("3")
sleep(1)
print("2")
sleep(1)
print("1")
sleep(1)
print("ended")

s.close()

print("Disconnected")

# End of file