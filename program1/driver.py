import sys
import Pyro4
import Pyro4.util
import threading
from Peer import Client
from ServerProxy import Server


def main():
    sys.excepthook = Pyro4.util.excepthook
    ns = Pyro4.locateNS()
    server_uri = ns.lookup("Main_Server")
    server = Pyro4.Proxy(server_uri)
    client_uri = ns.lookup("1")
    c1 = Pyro4.Proxy(client_uri)
    c1.obtain("exam")

if __name__=="__main__":
    main()

