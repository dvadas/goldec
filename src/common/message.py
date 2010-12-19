class MessageTypes(object):
	LOGIN, LOGIN_REPLY, NEW_GAME, ERROR = "Login", "LoginReply", "NewGame", "Error"

class GameTypes(object):
	DUEL, SOLO = "Duel", "Solo"

class InvalidMessageException(Exception):
	def __init__(self, errorMessage):
		self.errorMessage = errorMessage

def CatchMissingField(inner):
	def outer(self):
		try:
			return inner(self)
		except KeyError:
			raise InvalidMessageException("Malformed message. Missing field: %s" % inner.__name__[3:])
	return outer

class Message(object):
	_keyValueSeparator = ","
	_fieldSeparator = "|"

	def __init__(self, raw=None):
		self._fields = {}
		
		if raw != None:
			keyValues = raw.split(self._fieldSeparator)
			for keyValue in keyValues:
				try:
					key, value = keyValue.split(self._keyValueSeparator)
				except ValueError:
					raise InvalidMessageException(self.__init__)
				self._fields[key] = value

	def GetRaw(self):
		rawFields = []
		for key in self._fields:
			value = self._fields[key]
			value = value.replace(self._keyValueSeparator, "")
			value = value.replace(self._fieldSeparator, "")

			rawField = "%s%s%s" % (key, self._keyValueSeparator, value)
			rawFields.append(rawField)
		return self._fieldSeparator.join(rawFields)

	@CatchMissingField
	def GetType(self):
		return self._fields["Type"]
	def SetType(self, type):
		self._fields["Type"] = type

	@CatchMissingField
        def GetUsername(self):
                return self._fields["Username"]
        def SetUsername(self, username):
                self._fields["Username"] = username

	@CatchMissingField
        def GetSuccess(self):
                return self._fields["Success"] == "true"
        def SetSuccess(self, success):
		if success:
	                self._fields["Success"] = "true"
		else:
	                self._fields["Success"] = "false"

	@CatchMissingField
	def GetGameType(self):
                return self._fields["GameType"]
        def SetGameType(self, gameType):
                self._fields["GameType"] = gameType

	@CatchMissingField
	def GetErrorText(self):
                return self._fields["ErrorText"]
        def SetErrorText(self, errorText):
                self._fields["ErrorText"] = errorText


