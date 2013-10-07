from MetaData import *
from QueryHelper import *
from DownloadHelper import *
from ServerUtil import *
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
        self.download_folder = "downloads/"
        self.peers = dict()

        self.messages_received = dict()
        self.messages_sent = dict()
        self.files_to_download = dict()
        #message id = id_num + next_message_id
        self.next_message_id = 0

        self.download_queue = Queue.Queue()

        self.name_server= Pyro4.locateNS()
        self.file_server = None
        self.ip_address = 9000 + int(id_num)
        self.client_daemon = None
        self.query_helper = QueryHelper(self)
        self.download_helper = DownloadHelper(self)
        self.server_helper = ServerHelper(self)
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


    #### This intiates the Search
    def obtain(self,file_name):
        self.generate_query(file_name)


    #### put the job in the Queue
    def get_file(self,file_name,peer_port):
        if self.files_to_download.has_key(file_name) and peer_port in self.files_to_download[file_name]:
            self.download_queue.put((peer_port,file_name))
            getter = threading.Thread(target= self.download_file)
            getter.start()
            print "Starting download thread"
            return True
        else:
            return False


    ##### This is called in a seperate Thread, pulla job from the queue and
    #####download into the test_files folder, let the index know u have it
    def download_file(self):
        self.download_helper.download_file()

    #### Intially the peer id are taken in and the first
    #### the peer is contacted the proxy will be generated and stored
    def add_peer(self,peer_id):
        #print "\nFrom client : " + str(self.id_num) + " adding peer : " + str(peer_id)
        peer_port = 9000 + int(peer_id)
        self.peers[peer_port] = None

    def get_peer_proxys(self):
        for id in self.peers.keys():
            uri = self.name_server.lookup(str(id))
            self.peers[id] = Pyro4.Proxy(uri)

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

    def list_queries(self):
        for key in self.messages_sent.keys():
            print str(self.messages_sent[key]) + "\n"

    def start_client(self):
        daemon_thread = threading.Thread(target=self.server_helper.register_with_servers)
        daemon_thread.start()
        print "returning from start"

    def stop_client(self):
        self.file_server.stop_server()
        self.client_daemon.shutdown()
        print "Stopping client: " + str(self.id_num)




