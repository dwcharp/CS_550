from MetaData import *
from QueryHelper import *
from DownloadHelper import *
import Pyro4
import threading
import socket
import FileServer
import Queue
import time

Pyro4.config.SERIALIZER = 'pickle'
Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')
TTL = 10
class Client():

    def __init__(self,id_num):
        self.id_num = id_num
        self.meta_data = None
        self.download_folder = None
        self.peers = dict()

        self.messages_received = dict()
        self.messages_sent = dict()
        #message id = id_num + next_message_id
        self.next_message_id = 0

        self.download_queue = Queue.Queue()

        #self.name_server= Pyro4.locateNS()
        self.file_server = None
        self.ip_address = 9000 + int(id_num)
        self.client_daemon = None
        self.query_helper = QueryHelper(self)
        self.download_helper = DownloadHelper(self)
    #### This is called from other peers, and calls this on neigbhors

    #### This is called to generate a new query for this client
    def generate_query(self,file_name):
        mId = str(self.id_num) + str(self.next_message_id)
        self.next_message_id = self.next_message_id + 1
        self.query(mId,TTL,file_name,self.ip_address)


    def query(self,messageId,TTL,file_name,sender_info):
        self.query_helper.query(messageId,TTL,file_name,sender_info)

    ##### If peer as the file, send a hit query

    def send_hit_query(self,messageId,TTL,file_name,sender_info):
        self.query_helper.send_hit_query(messageId,TTL,file_name,sender_info)

    #### called from peer that is relaying a query message back
    def hit_query(self,messageId,TTL,file_name,sender_info):
        self.query_helper.hit_query(messageId,TTL,file_name,sender_info)


    #### This intiates the download process, exits if files is not on index
    def obtain(self,file_name):
        self.generate_query(file_name)
        '''if len(peer_with_file_id ) > 0:
            peer_uri = self.name_server.lookup(str(peer_with_file_id[0]))
            peer = Pyro4.Proxy(peer_uri)
            self.get_file(file_name,peer)
        else:
            print file_name + " is not on Index"'''


    #### Ask the peer for its ip information and put the job in the Queue
    def get_file(self,file_name,peer):
        self.download_queue.put((peer,file_name))
        getter = threading.Thread(target= self.download_file)
        getter.start()
        print "Starting download thread"


    ##### This is called in a seperate Thread, pulla job from the queue and
    #####download into the test_files folder, let the index know u have it
    def download_file(self):
        self.download_helper.download_file()

    def add_peer(self,peer_id,peer):
        #print "\nFrom client : " + str(self.id_num) + " adding peer : " + peer.id_num
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
        print "Client: " + str(self.id_num) + " : " +  str(self.meta_data.list_files())

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


