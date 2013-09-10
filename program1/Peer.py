from  ServerProxy import *
import Pyro4
import threading
class Client(object):

    def __init__(self,server):
        self.file_list = self.load_files()
        self.server = server
        self.run()

    def obtain(self,file_name):
        peers_with_file = self.server.search(file_name)
        print peers_with_file

    def load_files(self):
        return ["test","exam","year"]

    def get_id(self):
        while True:
            pass

    def register_with_server(self):
        self.id_num =self.server.generate_peer_id()
        self.server.registry(self.id_num, self.file_list)
        daemon = Pyro4.Daemon()
        client_uri = daemon.register(self)
        print "Client URI is : " + str(client_uri)
        ns = Pyro4.locateNS()
        ns.register(str(self.id_num),client_uri)
        daemon.requestLoop()

    def run(self):
        thread = threading.Thread(target=self.register_with_server())
        thread.setDaemon(True)
        thread.start()
