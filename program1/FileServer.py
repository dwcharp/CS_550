import SocketServer
import threading

class FileServerHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        self.data = self.rfile.readline().strip()
        print self.data + " from server !!!!"
        file  = open(directory + file_name + ".txt","wb+")
        self.request.sendall(file.read())
        file.close()



class ThreadFileServer(SocketServer.ThreadingMixIn,SocketServer.TCPServer):
    pass

class FileServer():
    def __init__(self,client):
        self.client = client
        self.server = None

    def start_server(self):
        HOST, PORT = "localhost",0

        self.server = ThreadFileServer((HOST,PORT),FileServerHandler)
        server_thread = threading.Thread(target=self.server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        return self.server.server_address

    def stop_server(self):
        self.server.shutdown()

def main():
    HOST, PORT = "localhost",9999
    server = FileServer((HOST,PORT),FileServerHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    while True:
        pass


