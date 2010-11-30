import SocketServer

from common.message import Message
from common.logging import Log
from common.config import HOST, PORT

_server = None
class TcpHandler(SocketServer.StreamRequestHandler):
	def handle(self):
		while True:
			raw = self.rfile.readline().strip()
			if raw == "":
				Log("Connection closed by %s" % (self.client_address[0]))
				return

			Log("Received data from %s - %s" % (self.client_address[0], raw))
			message = Message(raw)
			_server.Receive(message, self)

	def respond(self, message):
		self.wfile.write(message.ToRaw())

def RunServer(server):
	global _server
	_server = server

	socketServer = SocketServer.TCPServer((HOST, PORT), TcpHandler)
	socketServer.serve_forever()
