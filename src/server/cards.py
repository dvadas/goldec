from common.card import Action, Goal, Resource

class Cards(object):
	def __init__(self, actionsFilename, goalsFilename, resourcesFilename):
		self._actions = {}
		self._goals = {}
		self._resources = {}

		self._Load(self._actions, actionsFilename, Action)
		self._Load(self._goals, goalsFilename, Goal)
		self._Load(self._resources, resourcesFilename, Resource)

	def _Load(self, cards, filename, Klass):
		lineNumber = 0
		for line in file(filename):
			lineNumber += 1

			# Cut off the comment
			index = line.find("#")
			if (index != -1):
				line = line[:index]
			
			line = line.strip()
			if line == "":
				continue

			try:
				card = Klass(line)
			except Exception, e:
				print "Error on %s:%d - %s" % (filename, lineNumber, e)
				continue
			cards[card.GetName()] = card

