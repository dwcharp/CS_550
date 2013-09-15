from  Server import *
from MetaData import *
import Pyro4
import threading
import socket
import FileServer

class Client():

    def __init__(self):
        self.server = None
        self.file_server = FileServer.FileServer(self)
        print "Server: " + str(self.file_server.start_server())
        self.name_server=None
        self.id_num = 0
        self.client_daemon = None
        self.meta_data = None

    def obtain(self,file_name):
        peer_with_file_id = self.server.search(file_name)
        if len(peer_with_file_id ) > 0:
            peer = self.name_server.lookup(peer_with_file_id[0])
            self.get_file(file_name,peer)

    def get_file(self,file_name,peer):
        def download_file():
            print "Downloading file"
        peer_addr = peer.set_up_connection()
        getter = threading.Thread(target= download_file)
        getter.start()
        print "Starting thread"

    def set_up_connection(self):
        return

    def delete_file(self,file_name):
        self.server.remove_from_index(self.id_num,file_name)
        #delete from disk

    def set_meta_data(self, meta_data):
        self.meta_data = meta_data


    def register_with_server(self):
        self.name_server = Pyro4.locateNS()
        server_uri = self.name_server.lookup("Main_Server")
        self.server = Pyro4.Proxy(server_uri)
        self.id_num =self.server.generate_peer_id()
        self.server.registry(self.id_num, ["test"])
        self.client_daemon = Pyro4.Daemon()
        client_uri = self.client_daemon.register(self)
        print "Client URI is : " + str(client_uri)
        self.client_daemon.shutdown()
        self.name_server.register(str(self.id_num),client_uri)
        self.client_daemon.requestLoop()

    def start_client(self):
        daemon_thread = threading.Thread(target=self.register_with_server)
        daemon_thread.start()
        print "returning from start"

    def stop_client(self):
        print "Stopping client: " + str(self.id_num)

