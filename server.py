import socket
import multiprocessing as mp
from time import sleep

from classes  import OnlinePage

from game_constants.consts import HOST, PORT

class Server:
    def __init__(self):
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # solution for "[Error 89] Address already in use". Use before bind()
        self.s.bind((HOST, PORT))
        self.s.listen(1)
        
        self.clients = []
            
    def handle_client(self, conn, addr):
        print("[thread] starting")

        # do something
        message = b"Hello, client at " + addr[0].encode() + b" on port " + str(addr[1]).encode()
        conn.send(message)
        
        sleep(1)
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
        
        conn.close()

        print("[thread] ending")
    
    def run(self, q):
        try:
            print("Waiting for client")
            conn, addr = self.s.accept()
            
            print("Client:", addr)
                
            t = mp.Process(target=self.handle_client, args=(conn, addr))
            t.start()
            
            self.clients.append(t)
            q.put(t)
                
        except KeyboardInterrupt:
            print("Stopped by Ctrl+C")
        finally:
            if self.s:
                self.s.close()
            for t in self.clients:
                t.join()
    
    def stop(self):
        self.s.close()
        for t in self.clients:
            t.join()
    
    def get_players(self):
        return self.clients

if __name__ == "__main__":
    server = Server()
    # server.run()
    players = server.get_players()
    print(players)