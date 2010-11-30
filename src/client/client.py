from network import Connection
from common.message import Message, MessageTypes
from common.logging import Log

class Client(object):
	def __init__(self, connection, username):
		self._connection = connection
		self._running = True

		self._SendLogin(username)
		self._MainLoop()

	def _SendLogin(self, username):
		message = Message()
		message.SetType(MessageTypes.LOGIN)
		message.SetUsername(username)

		self._connection.Send(message)

	def _SendNewGame(self):
		message = Message()
		message.SetType(MessageTypes.NEW_GAME)

		self._connection.Send(message)

	def _MainLoop(self):
		while self._running:
			message, userInput = self._connection.Wait()
			if self._connection.IsClosed():
				break

			if message != None:
				Log("Received message in main loop - %s" % message.GetRaw())
				messageType = message.GetType()

				handler = getattr(self, "_Handle" + messageType)
				handler(message)

			if userInput != None:
				messageToSend = self._gameState.ProcessUserInput(userInput)
				self._connection.Send(messageToSend)

	def _RenderGameToUser(self):
		print self._gameState.GetText()

	def _HandleLoginReply(self, message):
		if message.IsSuccessful():
			Log("Logged in")
			self._SendNewGame()
			print "Waiting for game to start..."
		else:
			print >> sys.stderr, "Failed to login -", message.GetErrorText()
			self._running = False

	def _HandleUpdateGameState(self, message):
		self._gameState = message.GetGameState()
		self._RenderGameToUser()


