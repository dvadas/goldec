import os

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
		print message.GetType()
