import sys
import Pyro4
import Pyro4.util
import threading
from Peer import Client

sys.excepthook = Pyro4.util.excepthook
ns = Pyro4.locateNS()
server_uri = ns.lookup("Main_Server")
server = Pyro4.Proxy(server_uri)
c1 = Client(server)
c2 = Client(server)

self.id_num =self.server.generate_peer_id()
daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()
client_uri = daemon.register(c1)
print "Client URI is : " + str(client_uri)
ns.register(str(c1.id_num),client_uri)

client_uri = daemon.register(c2)
print "Client URI is : " + str(client_uri)
ns.register(str(c2.id_num),client_uri)
daemon.requestLoop()
c1.obtain("exam")
