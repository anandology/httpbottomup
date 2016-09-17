"""Hello World HTTP Server, written using pure sockets.
"""
import sys
import os
from socket import *

CRLF = b"\r\n"

def http_server(host, port):            
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(5)

    print("Started server on http://{}:{}/".format(host, port))

    with sock:
        while True:
            client, addr = sock.accept()
            handle_request(client, addr)

def read_request(sock):
    fileobj = sock.makefile('r')
    method, path = read_status_line(fileobj)
    headers = read_headers(fileobj)
    return method, path, headers

def read_status_line(fileobj):
    line = fileobj.readline()
    method, path, protocol = line.strip().split()
    return method, path

def read_headers(fileobj):
    # assuming there won't be any duplicate headers, storing them in a dictionary
    headers = {}
    while True:
        line = fileobj.readline().strip()
        if not line:
            break
        name, value = line.split(":", 1)
        headers[name.strip().lower()] = value.strip()
    return headers

def handle_request(sock, remote_addr):

    method, path, request_headers = read_request(sock)

    status = "200 OK"
    headers = [
        "Server: Simple HTTP Server",
        "Connection: Close",
        "Content-type: text/plain"
    ]
    body = b"Hello World\n"

    headers.append("Content-Length: {}".format(len(body)))

    sock.send(b"HTTP/1.1 " + status.encode('ascii') + CRLF)
    header_bytes = b"".join(h.encode('ascii') + CRLF for h in headers)
    sock.send(header_bytes)
    sock.send(CRLF)
    sock.send(body)
    sock.close()

def main():
    host = sys.argv[1]
    port = int(sys.argv[2])
    http_server(host, port)

if __name__ == '__main__':
        main()
