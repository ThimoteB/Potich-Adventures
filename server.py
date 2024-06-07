import socket
import select
import json
import multiprocessing as mp
from time import sleep
from game_server import GameServer

from game_constants.consts import HOST, PORT

class Server(object):
    def __init__(self) -> None:
        # server data
        self.hostname = HOST
        self.port = PORT
        self.read_list:list = []
        """Sockets list -> first socket is the server socket, the others are client sockets"""
        self.max_players:int = 1
        
        # game data
        self.start_status:bool = False
        self.pre_game_data:dict = {
            "players": [],
            "start": False
        }
    
    def broadcast(self, input:dict) -> bool:
        """This method allow to broadcast data to every players in the read list

        Args:
            data (dict): a dict of data to be sent
        """
        print(f'Broadcasting : {input}')
        data = json.dumps(input)
        for cli in self.read_list[1:]:
            cli.send(data.encode())
        return True
        
        
    def update_players_list(self) -> None:
        """Update the players list with active connections
        """
        self.pre_game_data["players"] = []
        # count active players
        for cli in self.read_list[1:]:
            self.pre_game_data["players"].append(cli.getpeername())
    
    def update_start_status(self) -> None:
        if len(self.read_list[1:]) == self.max_players:
            self.pre_game_data["start"] = True
            self.start_status = True
            self.broadcast(self.pre_game_data)
            print(f'Starting the game with {len(self.read_list)-1} players')
    
    def start(self) -> list[socket.socket]:
        """This method is used to start the game server and wait for client connection in order to start the game
        """
        server_socket:socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print("Listening on", server_socket.getsockname())

        self.read_list = [server_socket]
        
        
        while not self.start_status:
            # wait for client response/connexion
            # select : wait until something is happening in a descriptor (server or client socket)
            readable, writable, errored = select.select(self.read_list, [], [])
            for s in readable: # for each socket (server/client)
                if s is server_socket: # manage server socket
                    client_socket, address = server_socket.accept()
                    self.read_list.append(client_socket)
                    print("Connection from", address)
                    self.update_players_list()
                    if len(self.read_list[1:]) != self.max_players:
                        self.broadcast(self.pre_game_data)
                else: # manage client socket
                    data = s.recv(1024)
                    if data: # received data
                        data = data.decode()
                        print(f'Received from {s.getpeername()} : {data}')
                    else: # client closed connection
                        print("Disconnected :", s.getpeername())
                        s.close()
                        self.read_list.remove(s)
                        self.update_players_list()
                        self.broadcast(self.pre_game_data)
            self.update_start_status()
        return self.read_list
        

if __name__ == "__main__":
    while True:
        try:
            server = Server()
            game = GameServer(server.start())
        except Exception as e:
            print(f'Error : {e}')
            continue