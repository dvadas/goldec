from common.config import HOST, PORT
from common.network import CallbackFactory

from twisted.internet import reactor

def RunServer(server):
	reactor.listenTCP(PORT, CallbackFactory(None, None, server.Receive))
	reactor.run()

