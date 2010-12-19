from common.message import Message, MessageTypes, InvalidMessageException
from common.logging import Log

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver

class MessageProtocol(LineReceiver):
	def connectionMade(self):
		Log("Connected")
		if self.factory.onConnect is not None:
			self.factory.onConnect(self)
	def connectionLost(self, reason):
		Log("Disconnected")
		if self.factory.onDisconnect is not None:
			self.factory.onDisconnect()

	def lineReceived(self, line):
		Log("Received data: %s" % line)
		if self.factory.onReceive is not None:
			try:
				message = Message(line)
				self.factory.onReceive(message, self)
			except InvalidMessageException, e:
				response = Message()
				response.SetType(MessageTypes.ERROR)
				response.SetErrorText(e.errorMessage)
				self.sendMessage(response)

	def sendMessage(self, message):
		raw = message.GetRaw()
		Log("Sending data: %s" % raw)
		self.sendLine(raw)

class CallbackFactory(Factory):
	protocol = MessageProtocol

	def __init__(self, onConnect, onDisconnect, onReceive):
		self.onConnect = onConnect
		self.onDisconnect = onDisconnect
		self.onReceive = onReceive

