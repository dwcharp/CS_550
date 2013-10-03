class DownloadHelper:
    def __init__(self, client):
        self.client = client


#### This intiates the download process, exits if files is not on index
    def obtain(self,file_name):
        print "peer: " + str(peer_with_file_id)
        if len(peer_with_file_id ) > 0:
            peer_uri = self.client.name_server.lookup(str(peer_with_file_id[0]))
            peer = Pyro4.Proxy(peer_uri)
            self.client.get_file(file_name,peer)
        else:
            print file_name + " is not on Index"

#### Ask the peer for its ip information and put the job in the Queue
    def get_file(self,file_name,peer):
        peer_ip,peer_port = peer.get_addr()
        self.client.download_queue.put((peer_ip,peer_port,file_name))
        getter = threading.Thread(target= self.client.download_file)
        getter.start()
        print "Starting download thread"

##### This is called in a seperate Thread, pulla job from the queue and
#####download into the test_files folder, let the index know u have it
    def download_file(self):
        peer_ip,peer_port, file_name = self.client.download_queue.get()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        file  = open(self.client.download_folder + file_name + ".txt","wb+")
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
            self.client.server.add_file_to_index(self.client.id_num,file_name)
            self.client.meta_data.add_file(file_name)

        finally:
            file.close()
            sock.close()
