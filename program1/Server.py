import Pyro4
import sys
from MetaData import *
Pyro4.config.SERIALIZER = 'pickle'
Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')

class Server():

    def __init__(self):
        self.next_usable_id = 0
        self.peers = dict()
        self.peer_file_index = dict()
        self.server_daemon = None

    def registry(self,peer_id, ip,port, file_list):
        self.peers[peer_id] = (ip,port)

        for f in file_list:
            if self.peer_file_index.has_key(f.name):
                self.peer_file_index[f.name].append(peer_id)
            else:
                self.peer_file_index[f.name] = [peer_id]
            print self.peer_file_index

    def search(self,file_name):
        if self.peer_file_index.has_key(file_name):
            return self.peer_file_index[file_name]
        else:
            return []

    def remove_file_from_index(self, peer_id,file_name):
        if self.peer_file_index.has_key(file_name):
            self.peer_file_index[file_name].remove(peer_id)

    def generate_peer_id(self):
        self.next_usable_id  = self.next_usable_id + 1
        return self.next_usable_id

    def start_system(self):
        print "Starting Server"
        self.server_daemon = Pyro4.Daemon()
        server_uri = self.server_daemon.register(self)
        print "Server URI is : " + str(server_uri)
        ns = Pyro4.locateNS()
        ns.register("Main_Server",server_uri)
        self.server_daemon.requestLoop()

    def get_num_clients(self):
        return self.next_usable_id

    def stop_server(self):
        print "Stoppping server"
        self.server_daemon.shutdown()

def main():
    server =Server()
    server.start_system()


if __name__=="__main__":
    main()
