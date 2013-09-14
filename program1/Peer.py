from  Server import *
from MetaData import *
import Pyro4
import threading

class Client():

    def __init__(self):
        self.file_list = self.load_files()
        self.server = None
        self.name_server=None
        self.id_num = 0
        self.client_daemon = None
        self.meta_data = None

    def obtain(self,file_name):
        peer_with_file_id = self.server.search(file_name)
        #peer = self.name_server.lookup(peer_with_file_id)
        #peer.get_file(file_name)
        print peer_with_file_id

    def get_file(self,file_name):
        def download_file():
            print "Downloading file"

        getter = threading.Thread(target= download_file)
        getter.start()
        print "Starting thread"

    def delete_file(self,file_name):
        self.server.remove_from_index(self.id_num,file_name)
        #delete from disk
    def set_meta_data(self, meta_data)
        self.meta_data = meta_data

    def load_files(self,file_names):
        return file_names


    def register_with_server(self):
        self.name_server = Pyro4.locateNS()
        server_uri = self.name_server.lookup("Main_Server")
        self.server = Pyro4.Proxy(server_uri)
        self.id_num =self.server.generate_peer_id()
        self.server.registry(self.id_num, self.file_list)
        self.client_daemon = Pyro4.Daemon()
        client_uri = self.client_daemon.register(self)
        print "Client URI is : " + str(client_uri)
        self.name_server.register(str(self.id_num),client_uri)
        self.client_daemon.requestLoop()

    def start_client(self):
        daemon_thread = threading.Thread(target=self.register_with_server)
        daemon_thread.start()
        print "returning from start"

    def stop_client(self):
        self.client_daemon.shutdown()
        print "Stopping client: " + str(self.id_num)

