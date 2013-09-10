from  ServerProxy import *
import Pyro4
import threading
Pyro4.config.COMMTIMEOUT=20
class Client(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.file_list = self.load_files()
        self.server = None

    def obtain(self,file_name):
        peers_with_file = self.server.search(file_name)
        print peers_with_file

    def load_files(self):
        return ["test","exam","year"]

    def get_id(self):
        while True:
            pass

    def register_with_server(self):
        ns = Pyro4.locateNS()
        server_uri = ns.lookup("Main_Server")
        self.server = Pyro4.Proxy(server_uri)
        self.id_num =self.server.generate_peer_id()
        self.server.registry(self.id_num, self.file_list)
        daemon = Pyro4.Daemon()
        client_uri = daemon.register(self)
        print "Client URI is : " + str(client_uri)

        ns.register(str(self.id_num),client_uri)
        daemon.requestLoop()

    def run(self):
        self.register_with_server()

def main():
    client =Client()
    client.start()

    client1 =Client()
    client1.start()

if __name__=="__main__":
    main()
