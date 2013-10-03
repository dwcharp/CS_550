import SocketServer
import threading
import os
#### Open the file and send it to the client, the file is known to exist
class FileServerHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        test_folder = cwd + "/" + "test_files"
        self.data = self.rfile.readline().strip()
        print self.data + "\nfrom server !!!!"
        file_name = self.data
        try:
            file  = open(test_folder + file_name + ".txt","r")
            self.data = file.read()
            self.request.sendall(self.data)
        finally:
            file.close()


class ThreadFileServer(SocketServer.ThreadingMixIn,SocketServer.TCPServer):
    pass

class FileServer():
    def __init__(self,client):
        self.client = client
        self.server = None

    def start_server(self,port_num):
        HOST, PORT = "localhost",port_num
        self.server = ThreadFileServer((HOST,PORT),FileServerHandler)
        server_thread = threading.Thread(target=self.server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        return self.server.server_address

    def stop_server(self):
        self.server.shutdown()


def main():
    server = FileServer(None)
    print server.start_server(9999)
    # Exit the server thread when the main thread terminates
    while True:
        pass

if __name__ == '__main__':
    main()
