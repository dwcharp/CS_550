import Pyro4

class Server(object):

    def __init__(self):
        self.next_usable_id = 0
        self.peers = []
        self.peer_file_index = dict()

    def registry(self,peer_id, file_list):
        self.peers.append(peer_id)

        for file_name in file_list:
            if self.peer_file_index.has_key(file_name):
                self.peer_file_index[file_name].append(peer_id)
            else:
                self.peer_file_index[file_name] = [peer_id]
            print self.peer_file_index

    def search(self,file_name):
        if self.peer_file_index.has_key(file_name):
            return self.peer_file_index[file_name]
        else:
            return []

    def generate_peer_id(self):
        self.next_usable_id  = self.next_usable_id + 1
        return self.next_usable_id

def main():
    server = Server()
    Pyro4.Daemon.serveSimple(
        {
            server: "file.server"
        },
        ns = True)
if __name__=="__main__":
    main()
