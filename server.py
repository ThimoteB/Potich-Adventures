import socket
import select
import multiprocessing as mp
from time import sleep

from classes  import OnlinePage

from game_constants.consts import HOST, PORT

class Server(object):
    def __init__(self):
        self.hostname = HOST
        self.port = PORT
    
    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print("Listening on", server_socket.getsockname())

        read_list = [server_socket]
        new_con:bool = False
        while True:
            # server proces (do something)
            print("Do something")
            
            
            # wait for client response/connexion
            # select : wait until something is happening in a descriptor (server or client socket)
            readable, writable, errored = select.select(read_list, [], [])
            for s in readable:
                if s is server_socket and not new_con: # manage server socket
                    client_socket, address = server_socket.accept()
                    read_list.append(client_socket)
                    print("Connection from", address)
                    
                    # do something when a client join the server
                    data = str.encode("Total players : " + str(len(read_list)-1))
                    print(data)
                    for cli in read_list[1:]:
                        cli.send(data)
                else: # manage client socket
                    data = s.recv(1024)
                    print("received:", data)
                    if data:
                        s.send(data)
                        print("sent:", data)
                    else:
                        print("Closing connection")
                        s.close()
                        read_list.remove(s)
                        data = str.encode("Total players : " + str(len(read_list)-1))
                        print(data)
                        for cli in read_list[1:]:
                            cli.send(data)
    
        

if __name__ == "__main__":
    server = Server()
    try:
        server.start()
    except:
        print("Error/Stop")
    finally:
        for process in mp.active_children():
            process.terminate()
            process.join()