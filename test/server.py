import select
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('', 44440))
server_socket.listen(5)
print("Listening on", server_socket.getsockname())

read_list = [server_socket]
while True:
    readable, writable, errored = select.select(read_list, [], [])
    for s in readable:
        if s is server_socket:
            client_socket, address = server_socket.accept()
            read_list.append(client_socket)
            print("Connection from", address)
        else:
            data = s.recv(1024)
            print("received:", data)
            if data:
                s.send(data)
                print("sent:", data)
            else:
                print("Closing connection")
                s.close()
                read_list.remove(s)