import sys
import Pyro4
import Pyro4.util
from Peer import Client

sys.excepthook = Pyro4.util.excepthook
server = Pyro4.Proxy("PYRONAME:file.server")
c = Client(server)
