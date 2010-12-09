from network import RunClient

from common.message import Message, MessageTypes
from common.logging import Log

class Client(object):
	def __init__(self, username):
		self._username = username
		RunClient(self)

	def _SendLogin(self):
		message = Message()
		message.SetType(MessageTypes.LOGIN)
		message.SetUsername(self._username)

		Log("Logging in")
		self._connection.sendMessage(message)

	def _SendNewGame(self):
		message = Message()
		message.SetType(MessageTypes.NEW_GAME)

		self._connection.sendMessage(message)

	def Connect(self, connection):
		self._connection = connection
		self._SendLogin()

	def UserInput(self, line):
		Log("Received user input: %s" % line)

	def Receive(self, message, connection):
		messageType = message.GetType()

		handler = getattr(self, "_Handle" + messageType)
		response = handler(message, connection)
		if response is not None:
			client.sendMessage(response)

	def _RenderGameToUser(self):
		print self._gameState.GetText()

	def _HandleLoginReply(self, message, connection):
		if message.GetSuccess():
			Log("Logged in")
			self._SendNewGame()
			print "Waiting for game to start..."
		else:
			print >> sys.stderr, "Failed to login -", message.GetErrorText()
			self._running = False

	def _HandleUpdateGameState(self, message, connection):
		self._gameState = message.GetGameState()
		self._RenderGameToUser()


