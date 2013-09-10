import Pyro4
import threading
Pyro4.config.COMMTIMEOUT=60
class Server(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.next_usable_id = 0
        self.peers = []
        self.peer_file_index = dict()

    def registry(self,peer_id, file_list):
        self.peers.append(peer_id)

        for file_name in file_list:
            if self.peer_file_index.has_key(file_name):
                self.peer_file_index[file_name].append(peer_id)
            else:
                self.peer_file_index[file_name] = [peer_id]
            print self.peer_file_index

    def search(self,file_name):
        if self.peer_file_index.has_key(file_name):
            return self.peer_file_index[file_name]
        else:
            return []

    def generate_peer_id(self):
        self.next_usable_id  = self.next_usable_id + 1
        return self.next_usable_id

    def start_system(self):
        print "Starting Server"
        daemon = Pyro4.Daemon()
        server_uri = daemon.register(self)
        print "Server URI is : " + str(server_uri)
        ns = Pyro4.locateNS()
        ns.register("Main_Server",server_uri)
        daemon.requestLoop()

    def run(self):
        self.start_system()

def main():
    server =Server()
    server.start()

if __name__=="__main__":
    main()
