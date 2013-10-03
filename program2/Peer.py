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
        self.id_num = None
        self.meta_data = MetaData("this",[])
        self.download_folder = None
        self.create_downloads_folder()
        self.peers = dict()
        self.messages_received = dict()
        self.messages_sent = dict()
        self.download_queue = Queue.Queue()
        #self.name_server= Pyro4.locateNS()
        self.file_server = None
        self.ip_address = None
        self.client_daemon = None

#### This is called from other peers, and calls this on neigbhors

    def query(self,messageId,TTL,file_name,sender_info):
        if self.messages_received.has_key(messageId) or self.messages_sent.has_key(messageId):
            print "Not sending query from " + str(self.ip_address)
            return
        else:
            if self.ip_address == sender_info:
                self.messages_sent[messageId] = True
            else:
                self.messages_received[messageId] = sender_info
        if TTL > 0:
            TTL = TTL -1
            for peer in self.peers.values():
                peer.query(messageId,TTL,file_name,self.ip_address)

        if self.meta_data.has_file(file_name):
            self.send_hit_query(messageId,TTL,file_name,self.ip_address)
##### If peer as the file, send a hit query

    def send_hit_query(self,messageId,TTL,file_name,sender_info):
        print "Sending a Hit for: " + file_name + " from client: " + str(self.ip_address) + " orgin: " + str(sender_info)
        peer_info = self.messages_received[messageId]
        peer = self.peers[peer_info]
        peer.hit_query(messageId,TTL,file_name,sender_info)

    #### called from peer that is relaying a query message back
    def hit_query(self,messageId,TTL,file_name,sender_info):
        if self.messages_sent.has_key(messageId):
            print str(sender_info) + " has the file from client" + str(self.ip_address)
            #### download file
        else:
            self.send_hit_query(messageId,TTL,file_name,sender_info)
            pass


#### This intiates the download process, exits if files is not on index
    def obtain(self,file_name):
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
        file  = open(self.download_folder + file_name + ".txt","wb+")
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

    def add_peer(self,peer_id,peer):
        self.peers[peer_id] = peer

    def get_addr(self):
        return (self.ip,self.port)

    def delete_file(self,file_name):
        self.meta_data.remove_file(file_name)
        #delete from disk

    def set_meta_data(self, meta_data):
        self.meta_data = meta_data

    def add_file(self,file_name):
        self.meta_data.add_file(file_name)

    def list_files_on_index(self):
        pass


    ###### Helper functions ######

    #### This is started in a seperate thread ####
    def register_with_servers(self):
        self.client_daemon = Pyro4.Daemon()
        self.start_file_server()
        self.register_to_naming_server()
        self.client_daemon.requestLoop()

    def register_to_naming_server(self):
        client_uri = self.client_daemon.register(self)
        ip,port = self.ip_address
        self.name_server.register(str(ip) + str(port),client_uri)


    def start_file_server(self):
        self.file_server = FileServer.FileServer(self)
        self.ip_address = self.file_server.start_server()

    def start_client(self):
        daemon_thread = threading.Thread(target=self.register_with_servers)
        daemon_thread.start()
        print "returning from start"

    def stop_client(self):
        self.file_server.stop_server()
        self.client_daemon.shutdown()
        print "Stopping client: " + str(self.id_num)

def create_downloads_folder(self):
        cwd = os.getcwd()
        self.download_folder = download_folder = cwd + "/" + "downloads"
        if  not os.path.exists(download_folder):
            os.mkdir(download_folder)
        else:
            print "Folder exist"
def main():
    c1 = Client()
    c2 = Client()
    c3 = Client()
    c1.ip_address = "1"
    c2.ip_address = "2"
    c3.ip_address = "3"
    c1.add_file("Book of Murphy")
    c2.add_file("Book of Tina")
    c3.add_file("Book of Fey")
    c1.add_peer("2",c2)
    c2.add_peer("3",c3)
    c2.add_peer("1",c1)
    c3.add_peer("2",c2)
    c1.query("1",10,"Book of Fey","1")
    c3.query("2",10,"Book of Tina","3")
    c3.query("5",10,"Book of Murphy","3")
    c2.query("9",10,"Book of Murphy","2")

if __name__=="__main__":
    main()


