#!/usr/bin/env python

import sys

from client.client import Client
from common.logging import LogInit

def main(args):
	LogInit("-")

	username = args[1]
	client = Client(username)

if __name__ == "__main__":
	main(sys.argv)
