class MessageTypes(object):
	LOGIN, LOGIN_REPLY, NEW_GAME = "Login", "LoginReply", "NewGame"

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

        def GetUsername(self):
                return self._fields["Username"]
        def SetUsername(self, username):
                self._fields["Username"] = username

        def GetSuccess(self):
                return self._fields["Success"] == "true"
        def SetSuccess(self, success):
		if success:
	                self._fields["Success"] = "true"
		else:
	                self._fields["Success"] = "false"

