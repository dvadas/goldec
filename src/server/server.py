import os

from common.message import Message, MessageTypes
from common.logging import Log

from cards import Cards
import network

class Server(object):
	def __init__(self, dataDir):
		self._LoadData(dataDir)

		network.RunServer(self)

	def _LoadData(self, dataDir):
		actionsFilename = os.path.join(dataDir, "actions")
		goalsFilename = os.path.join(dataDir, "goals")
		resourcesFilename = os.path.join(dataDir, "resources")

		self.cards = Cards(actionsFilename, goalsFilename, resourcesFilename)

	def Receive(self, message, client):
		messageType = message.GetType()

		handler = getattr(self, "_Handle" + messageType)
		response = handler(message, client)
		if response is not None:
			client.sendMessage(response)

	def _HandleLogin(self, message, client):
		response = Message()
		response.SetType(MessageTypes.LOGIN_REPLY)

		username = message.GetUsername()
		success = self._VerifyLogin(username)
		response.SetSuccess(success == "")
		if success == "":
			Log("User %s successfully logged in" % username)
			#self._users[client] = User(username)
		else:
			Log("User %s failed login: %s" % username, success)
			response.SetErrorText(success)
		return response

	def _HandleNewGame(self, message, client):
		Log("Starting new game")

	# TODO: Add passwords, encryption, etc
	# Return an error message explaining failure, or empty string on success
	def _VerifyLogin(self, username):
		return ""

