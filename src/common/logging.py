import sys
import datetime

_logFile = None
def LogInit(logFilename):
	global _logFile
	if logFilename == "-":
		_logFile = sys.stdout
	else:
		_logFile = open(logFilename)

def Log(line):
	now = datetime.datetime.now()
        _logFile.write("[%s] %s\n" % (now, line))
