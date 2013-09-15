rom  Server import *
from MetaData import *
import Pyro4
import threading
import socket

class ClientProxy():
    def __init__(self, client):
        self.client = client
        self.server = None
        self.start_client()

    def get_server(self):
        return server

     def register_with_server(self):
        client = self.client
        self.name_server = Pyro4.locateNS()
        server_uri = self.name_server.lookup("Main_Server")
        self.server = Pyro4.Proxy(server_uri)
        client.id_num =self.server.generate_peer_id()
        self.server.registry(client.id_num,client.file_list)
        self.client_daemon = Pyro4.Daemon()
        client_uri = self.client_daemon.register(client)
        print "Client URI is : " + str(client_uri)
        self.name_server.register(str(client.id_num),client_uri)
        self.client_daemon.requestLoop()

    def start_client(self):
        daemon_thread = threading.Thread(target=self.register_with_server)
        daemon_thread.start()
        print "returning from start"

    def stop_client(self):
        self.client_daemon.shutdown()
        print "Stopping client: " + str(self.id_num)
