import os

from common.message import Message, MessageTypes
from common.logging import Log

from cards import Cards
from user import User
import network

class Server(object):
	def __init__(self, dataDir):
		# Map a common.network.MessageProtocol to a User
		self._users = {}
		# A user requests a new game, then has to wait for another user
		# to also want a name game
		self._userWaitingForNewGame = None

		# Map a game id to a Game
		self._games = {}

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
			user = User(username, client)
			self._users[client] = user
		else:
			Log("User %s failed login: %s" % username, success)
			response.SetErrorText(success)
		return response

	def _HandleNewGame(self, message, client):
		try:
			user = self._users[client]
		except KeyError:
			Log("Client is not logged in")
			raise InvalidMessageException("You are not logged in.")

		gameType = message.GetGameType()
		Log("User %s wants a new game with type %s" % (user.GetName(), gameType)) 

		if self._userWaitingForNewGame == None:
				self._userWaitingForNewGame = user
				Log("User %s is now waiting for a new game" % user.GetName())
		else:
			Log("Starting new game between %s and %s" % (self._userWaitingForNewGame.GetName(), user.GetName()))
			self._userWaitingForNewGame = None

			game = _StartNewGame(self._userWaitingForNewGame, user)
			gameId = uuid.uuid1()
			self._games[gameId] = game

			self._SendGameStateToUsers(game)

	def _SendGameStateToUsers(self, game):
		for user in game.GetUsers():
			state = game.GetState(user)
			response = state.ToMessage()
			user.GetClient().sendMessage(response)

	# TODO: Add passwords, encryption, etc
	# Return an error message explaining failure, or empty string on success
	def _VerifyLogin(self, username):
		return ""

