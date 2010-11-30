#!/usr/bin/env python

import sys

from client.network import Connection
from client.client import Client
from common.logging import LogInit

def main(args):
	LogInit("-")

	username = args[1]
	connection = Connection()
	client = Client(connection, username)

if __name__ == "__main__":
	main(sys.argv)
