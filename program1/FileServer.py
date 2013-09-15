import SocketServer
import threading

class FileServerHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        self.data = self.rfile.readline().strip()
        print self.data
        #self.request.sendall(self.data)



class ThreadFileServer(SocketServer.ThreadingMixIn,SocketServer.TCPServer):
    pass

class FileServer():
    def __init__(self,client):
        self.client = client

    def start_server(self):
        HOST, PORT = "localhost",0

        server = ThreadFileServer((HOST,PORT),FileServerHandler)
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        return server.server_address

def main():
    HOST, PORT = "localhost",9999
    server = FileServer((HOST,PORT),FileServerHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    while True:
        pass


