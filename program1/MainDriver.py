import Pyro4
import Pyro4.util
import threading
from Peer import Client
from ServerProxy import Server
import time


def main():
    ns = Pyro4.locateNS()
    server_uri = ns.lookup("Main_Server")
    server = Pyro4.Proxy(server_uri)
    server._pyroOneway.add("stop_server")
    client_uri = ns.lookup("1")
    c1 = Pyro4.Proxy(client_uri)
    c1._pyroOneway.add("stop_client")
    c1.get_file("test")
    c1.stop_client()
    server.stop_server()



if __name__=="__main__":
    main()

