import sys

from twisted.internet import reactor
from twisted.internet import stdio
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver

from common.logging import Log
from common.config import HOST, PORT
from common.network import MessageProtocol, CallbackFactory

class MessageClientFactory(ClientFactory):
	def __init__(self, callbackFactory):
		self._callbackFactory = callbackFactory

	def startedConnecting(self, connector):
		Log("Connecting to server")

	def buildProtocol(self, addr):
		connection = MessageProtocol()
		connection.factory = self._callbackFactory
		return connection

	def clientConnectionLost(self, connector, reason):
		Log("Lost connection to server. Reason: %s" % reason)

	def clientConnectionFailed(self, connector, reason):
		Log("Connection failed to server. Reason: %s" % reason)

class UserInputProtocol(LineReceiver):
	from os import linesep as delimiter

	def __init__(self, callback):
		self._callback = callback

	def connectionMade(self):
		self.transport.write('>>> ')

	def lineReceived(self, line):
		self._callback(line)
		self.transport.write('>>> ')
	
def RunClient(client):
	callbackFactory = CallbackFactory(client.Connect, None, client.Receive)
	reactor.connectTCP(HOST, PORT, MessageClientFactory(callbackFactory))
	stdio.StandardIO(UserInputProtocol(client.UserInput))
	reactor.run()

