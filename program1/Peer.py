from  ServerProxy import *

class Client(object):

    def __init__(self,server):
        self.file_list = self.load_files()
        self.server = server
        self.id_num =self.server.generate_peer_id()
        self.server.registry(self.id_num,self.file_list)

    def obtain(self,file_name):
        print "File"

    def load_files(self):
        return ["test","exam","year"]

