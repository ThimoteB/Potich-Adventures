import socket
import select
import json
import multiprocessing as mp
from time import sleep

from game_constants.consts import HOST, PORT

class Server(object):
    def __init__(self):
        self.hostname = HOST
        self.port = PORT
        self.read_list = []
    
    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print("Listening on", server_socket.getsockname())

        self.read_list = [server_socket]
        
        
        while True:
            # server proces (do something)
            
            
            # wait for client response/connexion
            # select : wait until something is happening in a descriptor (server or client socket)
            readable, writable, errored = select.select(self.read_list, [], [])
            for s in readable:
                if s is server_socket: # manage server socket
                    client_socket, address = server_socket.accept()
                    self.read_list.append(client_socket)
                    print("Connection from", address)
                    
                    # do something when a client join the server
                    # data = str.encode("Total players : " + str(len(self.read_list)-1))
                    data:dict = {
                        "players": []
                    }
                    for cli in self.read_list[1:]:
                        data["players"].append(cli.getpeername())
                    print(data)
                    data = json.dumps(data)
                    for cli in self.read_list[1:]:
                        cli.send(data.encode())
                else: # manage client socket
                    data = s.recv(1024)
                    if data:
                        print(data.decode())
                    else:
                        print("Closing connection")
                        s.close()
                        self.read_list.remove(s)
                        data = str.encode("Total players : " + str(len(self.read_list)-1))
                        print(data)
                        for cli in self.read_list[1:]:
                            cli.send(data)
        

if __name__ == "__main__":
    server = Server()
    # try:
    server.start()
        
    # except:
    #     print("Error/Stop")
    # finally:
    #     for process in mp.active_children():
    #         process.terminate()
    #         process.join()