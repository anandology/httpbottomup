"""Solution to the urlopen problem.

Write a function urlopen that takes an URL as argument and returns its contents.
"""

from socket import socket, AF_INET, SOCK_STREAM

def urlopen(url):
	"""Returns contents of a URL.
	"""
	protocol, host, port, path = urlsplit(url)

	sock = socket(AF_INET, SOCK_STREAM)
	sock.connect((host, port))

	CRLF = "\r\n"

	req = "".join([
		"GET ", path, " HTTP/1.1", CRLF,
		"Host: ", host, CRLF,
		"Connection: close", CRLF,
		"User-Agent: urlopen/0.1", CRLF,
		CRLF
	])
	sock.send(req.encode('ascii'))
	return HTTPResponse(sock)

class HTTPResponse:
	"""HTTP Response object. 

	Contains status, reason, headers and body fields.
	"""
	def __init__(self, sock):
		self._sock = sock
		self._init()
		self._read()

	def _init(self):
		self.status = 200
		self.reason = 'OK'
		self.headers = []
		self.body = ''

	def _read(self):
		self.fileobj = self._sock.makefile('rb')

		# read status line
		line = self.fileobj.readline()
		self.set_status_line(line)

		# read header lines
		while True:
			line = self.fileobj.readline()
			if not line.strip():
				break
			self.add_header_line(line)

		# read the body
		self.body = self.fileobj.read()

	def set_status_line(self, line):
		_, self.status, self.reason = line.strip().decode('ascii').split(None, 2)

	def add_header_line(self, line):
		key, value = line.decode('ascii').split(":", 1)
		self.headers.append((key.strip(), value.strip()))


def urlsplit(url):
	"""Splits the url into protocol, host, port and path.
	"""	
	protocol, rest = url.split("://", 1)
	host, path = rest.split("/", 1)
	path = "/" + path
	if ":" in host:
		host, port = host.split(":", 1)
		port = int(port)
	else:
		port = 80

	return protocol, host, port, path

def test_urlsplit():
	assert urlsplit("http://google.com/search") == ('http', 'google.com', 80, '/search')
	assert urlsplit("http://google.com:1234/search") == ('http', 'google.com', 1234, '/search')
	assert urlsplit("http://google.com:1234/") == ('http', 'google.com', 1234, '/')
