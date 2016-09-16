import argparse
import re
import os
import time
import mimetypes
from socket import *

re_first_line = re.compile("(GET|POST) ([^ ]+) HTTP/1.1")
CRLF = b"\r\n"

class HTTPServer:
    SERVER_NAME = "MyHttpd"

    def __init__(self, options):
        self.host = options.hostname
        self.port = options.port
        self.document_root = options.document_root
        self.sock = None

    def start(self):
        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            self.sock.bind((self.host, self.port))
            print("Started server on http://{}:{}/".format(self.host, self.port))
            self.sock.listen(5)

            while True:
                client, addr = self.sock.accept()
                with client:
                    req = HTTPRequest(client, addr)
                    req.read()
                    print("{} {} {}".format(time.asctime(), req.method, req.path))

                    response = self.handle_request(req)
                    response.send(client)
        except KeyboardInterrupt:
            self.sock.shutdown(SHUT_RDWR)

    def handle_request(self, req):
        if req.method != 'GET':
            return HTTPResponse('405 Method Not Allowed')

        if ".." in req.path:
            return HTTPResponse("404 Not Found")

        fullpath = self.document_root + req.path
        if not os.path.exists(fullpath):
            return HTTPResponse("404 Not Found")

        if os.path.isdir(fullpath):
            return self.handle_directory(req, fullpath)
        else:
            return self.handle_file(req, fullpath)

    def handle_file(self, req, fullpath):
        response = HTTPResponse()
        response.guess_content_type(fullpath)
        response.body = open(fullpath, 'rb').read()
        return response

    def handle_directory(self, req, fullpath):
        if not fullpath.endswith("/"):
            return HTTPResponse("302 Found", [("Location", req.path + "/")])
        files = os.listdir(fullpath)
        response = HTTPResponse()
        body_text = "".join('<a href="{}">{}</a><br>\n'.format(f, f) for f in files)
        response.body = body_text.encode('ascii')
        return response

class HTTPResponse:
    def __init__(self, status='200 OK', headers=None, body=b''):
        self.status = status
        self.headers = headers or []
        self.body = body

    def add_header(self, name, value):
        self.headers.append((name, value))

    def send(self, sock):
        self.add_special_headers()

        fileobj = sock.makefile('wb')
        with fileobj:
            self.send_status(fileobj)
            self.send_headers(fileobj)
            self.send_body(fileobj)

    def guess_content_type(self, path):        
        content_type, encoding = mimetypes.guess_type(path)
        self.add_header('Content-Type', 'content-type')

    def add_special_headers(self):
        names = set([name.lower() for name, value in self.headers])
        if 'server' not in names:
            self.add_header('Server', HTTPServer.SERVER_NAME)
        if 'content-type' not in names:
            self.add_header('Content-Type', 'text/html')
        if 'content-length' not in names:
            self.add_header('Content-Length', len(self.body))
        if 'connection' not in names:
            self.add_header('Connection', 'Close')

    def send_status(self, fileobj):
        fileobj.write(b"HTTP/1.1 " + self.status.encode('ascii') + CRLF)

    def send_headers(self, fileobj):
        for k, v in self.headers:
            header_bytes = '{}: {}'.format(k, v).encode('ascii')
            fileobj.write(header_bytes + CRLF)
        fileobj.write(CRLF)

    def send_body(self, fileobj):
        fileobj.write(self.body)

class HTTPRequest:
    def __init__(self, sock, remote_addr):
        self.sock = sock
        self.remote_addr = remote_addr
        self.method = 'GET'
        self.path = ''
        self.headers = []

    def read(self):
        fileobj = self.sock.makefile('r')
        with fileobj:
            self.method, self.path = self.read_first_line(fileobj)
            self.headers = self.read_headers(fileobj)

    def read_first_line(self, fileobj):
        line = fileobj.readline()
        m = re_first_line.match(line)
        if not m:
            raise Exception("Bad Status Line")

        # Doesn't support query strings
        method, path = m.groups()
        return method, path

    def read_headers(self, fileobj):
        headers = []
        while True:
            line = fileobj.readline()
            if not line.strip():
                break
            name, value = line.split(":", 1)
            headers.append((name.strip(), value.strip()))
        return headers

    def __repr__(self):
        return "<HTTPRequest(method=%r, path=%r, headers=%r)>" % (self.method, self.path, self.headers)

def parse_args():
    p = argparse.ArgumentParser(description="Simple HTTP Server")
    p.add_argument("-H", "--hostname", 
        help="Host name to bind, defaults to localhost",
        default="localhost")
    p.add_argument("-p", "--port", 
        help="Port to bind, defaults to %(default)s", 
        type=int, 
        default=8000)

    p.add_argument("-d", "--document-root", 
        help="Path to the document root (default: %(default)s)", 
        default=".")

    return p.parse_args()

def main():
    args = parse_args()
    server = HTTPServer(args)
    server.start()

if __name__ == '__main__':
        main()