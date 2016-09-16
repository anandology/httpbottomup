
# Internet Applications
[&larr; Back](.)

Lets see how to build internet applications using Python. We'll start building a client.

## Introduction to Sockets in Python

First lets create a simple TCP socket on IPv4.

	>>> import socket
	>>> sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

Since we are building a client, we need to connect to a server.

	>>> sock.connect(("http00.pipal.in", 13))

The `connect` function takes the (host, port) pair as argument.	Now we can receive whatever the server sends.

	>>> response = sock.recv(1024)
	>>> response
	b'16 SEP 2016 00:41:24 UTC\r\n'

Whatever we send or receive from a socket is always bytes. We need to encode/decode that into string if we want to print them.

	>>> response_text = response.decode('ascii')
	>>> print(response_text)
	16 SEP 2016 00:41:24 UTC

**Exercise:** Write an echo client program that takes host name as argument and sends a message`Hello Socket` to the echo server running on port 7 on that host and prints the response back.

	$ python echo_client.py http00.pipal.in
	Hello Socket

