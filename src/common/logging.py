import sys

_logFile = None
def LogInit(logFilename):
	global _logFile
	if logFilename == "-":
		_logFile = sys.stdout
	else:
		_logFile = open(logFilename)

def Log(line):
	_logFile.write(line + "\n")
