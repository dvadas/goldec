import socket
import sys
import select
from array import array

from common.logging import Log
from common.config import HOST, PORT

class Connection(object):
	def __init__(self):
		self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._socket.connect((HOST, PORT))
		self._isOpen = True

		self._recvBuffer = array("b")

	def Send(self, message):
		raw = message.GetRaw()
		self._socket.send(raw + "\n")

	def Receive(self):
		bytesRead = self._socket.recv_into(self._recvBuffer)
		if bytesRead == 0:
			Log("Connection closed by server")
			self._isOpen = False
			return

		#while true:
		#	received = self._socket.recv(1024)
		#	if len(received) == 0:
		#		break
		#	self._recvBuffer += received

		index = self._recvBuffer.find("\n")
		if index == -1:
			return None

		result = self._recvBuffer[:index]
		self._recvBuffer = self._recvBuffer[index + 1:]
		return Message(result)
	
	# Block until a message is ready
	def Wait(self):
		while True:
			reads, writes, exceptions = select.select([self._socket, sys.stdin], [], [])

			for readFile in reads:
				if readFile == self._socket:
					message = self.Receive()
					return message, None
				elif readFile == sys.stdin:
					line = sys.stdin.readline()
					line = line.strip()

					return None, line

	def IsClosed(self):
		return not self._isOpen

	def __del__(self):
		self._socket.close()

