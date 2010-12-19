
class User(object):
	def __init__(self, name, client):
		self._name = name
		self._client = client

	def GetName(self):
		return self._name
	def GetClient(self):
		return self._client
