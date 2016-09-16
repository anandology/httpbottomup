"""Python client to UNIX daytime service.

USAGE: 	python daytime.py HOSTNAME

For example:

	python daytime.py http00.pipal.in
	python daytime.py time-c.nist.gov
"""
import sys
import socket

# The standard port for daytime service is 13
DAYTIME_PORT = 13

def daytime(host):
	# create a network socket speaking TCP
	# * AF_INET - Network socket, the other option is Unix domain socket
	# * SOCK_STREAM - using TCP protocol, the other option is to use SOCK_DGRAM for UDP
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# connect to the specfied host
	sock.connect((host, DAYTIME_PORT))

	# Read some bytes, assuming that date will not be longer than 1024 bytes
	response_bytes = sock.recv(1024)
	print("Got response: %r" % response_bytes)

	# Reponse will always be in bytes. We need to convert into a string
	# so that we can print it.
	# We know that it has simple ASCII text so using that encoding.
	response_text = response_bytes.decode('ascii')
	return response_text.strip()

def main():
	host = sys.argv[1]
	response = daytime(host)
	print(response)

if __name__ == '__main__':
	main()