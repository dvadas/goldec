
class Card(object):
	def __init__(self, name):
		self._name = name

	def GetName(self):
		return self._name

_actionTypes = set(["Immediate", "Permanent", "Attack", "Reaction"])
class Action(Card):
	def __init__(self, line):
		name, type, text, price, playCost = line.split("\t")
		super(Action, self).__init__(name)

		if type not in _actionTypes:
			raise Exception("Invalid action type: " + type)
		self._type = type

		self._text = text
		self._price = int(price)
		self._playCost = int(playCost)

class Goal(Card):
	def __init__(self, line):
		name, text, reward = line.split("\t")
		super(Goal, self).__init__(name)

		self._text = text
		self._reward = int(reward)
		
class Resource(Card):
	def __init__(self, line):
		name, price, money, time = line.split("\t")
		super(Resource, self).__init__(name)

		self._price = int(price)
		self._money = int(money)
		self._time = int(time)
