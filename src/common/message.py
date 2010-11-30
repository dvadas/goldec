class MessageTypes(object):
	LOGIN, NEW_GAME = "Login", "NewGame"

class Message(object):
	def __init__(self, raw=None):
		self._fields = {}
		
		if raw != None:
			keyValues = raw.split("|")
			for keyValue in keyValues:
				key, value = keyValue.split(",")
				self._fields[key] = value

	def GetRaw(self):
		rawFields = []
		for key in self._fields:
			rawField = "%s,%s" % (key, self._fields[key])
			rawFields.append(rawField)
		return "|".join(rawFields)

	def GetType(self):
		return self._fields["Type"]
	def SetType(self, type):
		self._fields["Type"] = type

	def SetUsername(self, username):
		self._fields["Username"] = username

