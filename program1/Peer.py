from  Server import *
from MetaData import *
import Pyro4
import threading
import socket
import FileServer
import Queue
import time

Pyro4.config.SERIALIZER = 'pickle'
Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')

class Client():

    def __init__(self):
        self.name_server= Pyro4.locateNS()
        self.server = None
        self.id_num = None
        self.register_to_indexing_server()
        self.file_server = None
        self.client_daemon = None
        self.meta_data = None
        self.download_queue = Queue.Queue()

#### This intiates the download process, exits if files is not on index
    def obtain(self,file_name):
        peer_with_file_id = self.server.search(file_name)
        print "peer: " + str(peer_with_file_id)
        if len(peer_with_file_id ) > 0:
            peer_uri = self.name_server.lookup(str(peer_with_file_id[0]))
            peer = Pyro4.Proxy(peer_uri)
            self.get_file(file_name,peer)
        else:
            print file_name + " is not on Index"

#### Ask the peer for its ip information and put the job in the Queue
    def get_file(self,file_name,peer):
        peer_ip,peer_port = peer.get_addr()
        self.download_queue.put((peer_ip,peer_port,file_name))
        getter = threading.Thread(target= self.download_file)
        getter.start()
        print "Starting download thread"

##### This is called in a seperate Thread, pulla job from the queue and
#####download into the test_files folder, let the index know u have it
    def download_file(self):
        peer_ip,peer_port, file_name = self.download_queue.get()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        file  = open(self.get_working_dir() + file_name + ".txt","wb+")
        try:
            print "\nConnecting to fileserver!!!!\n"
            sock.connect((peer_ip,peer_port))
            sock.sendall(file_name + "\n")
            while 1:
                file_data = sock.recv(1024)
                if not file_data:
                    print "\nData was empty"
                    break
                else:
                    print file_data
                    file.write(file_data)
            self.server.add_file_to_index(self.id_num,file_name)
            self.meta_data.add_file(file_name)

        finally:
            file.close()
            sock.close()

    def list_files_on_index(self):
        index = self.server.list_index()
        for key in index:
            print key

    def get_addr(self):
        return (self.ip,self.port)

    def get_id(self):
        return self.id_num

    def delete_file(self,file_name):
        self.server.remove_file_from_index(self.id_num,file_name)
        self.meta_data.remove_file(file_name)
        #delete from disk

    def set_meta_data(self, meta_data):
        self.meta_data = meta_data

    def get_file_names(self):
        return self.meta_data.files

    def get_working_dir(self):
        return self.meta_data.working_directory




    ###### Helper functions ######

    #### This is started in a seperate thread ####
    def register_with_servers(self):
        self.client_daemon = Pyro4.Daemon()
        self.start_file_server()
        self.server.registry(self.id_num,self.ip,self.port
            ,self.meta_data.files)
        self.register_to_naming_server()
        self.client_daemon.requestLoop()

    #### Get a id from the Index Server and then use this in the Naming Server
    def register_to_indexing_server(self):
        server_uri = self.name_server.lookup("Main_Server")
        self.server = Pyro4.Proxy(server_uri)
        self.id_num =self.server.generate_peer_id()


    def register_to_naming_server(self):
        client_uri = self.client_daemon.register(self)
        self.name_server.register(str(self.id_num),client_uri)


    def start_file_server(self):
        self.file_server = FileServer.FileServer(self)
        self.ip , self.port = self.file_server.start_server()

    def start_client(self):
        daemon_thread = threading.Thread(target=self.register_with_servers)
        daemon_thread.start()
        print "returning from start"

    def stop_client(self):
        self.file_server.stop_server()
        self.client_daemon.shutdown()
        print "Stopping client: " + str(self.id_num)

def main():
    c1 = Client()
    c2 = Client()
    c1.start_client()

if __name__=="__main__":
    main()


