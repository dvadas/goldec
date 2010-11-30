#!/usr/bin/env python

import sys
import server.network

from server.server import Server
from common.logging import LogInit

def main(args):
	LogInit("-")

	dataDir = args[1]
	server = Server(dataDir)

if __name__ == "__main__":
	main(sys.argv)
