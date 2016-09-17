"""Simple HTTP Server Library.

USAGE:

    from httpserver import start_server

    def handle_request(method, path, headers):
        return "200 OK", [("Content-type": "text/plain")], b'Hello World!'

    start_server('localhost', 8080, handle_request)

"""
import sys
import os
from socket import *

CRLF = b"\r\n"

def start_server(host, port, handle_request):            
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(5)

    print("Started server on http://{}:{}/".format(host, port))

    with sock:
        while True:
            client, addr = sock.accept()
            method, path, req_headers = read_request(client)
            status, headers, body = handle_request(method, path, req_headers)
            write_response(client, status, headers, body)
            client.close()

def read_request(sock):
    fileobj = sock.makefile('r')
    method, path = read_status_line(fileobj)
    headers = read_headers(fileobj)
    fileobj.close()
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

def write_response(sock, status, headers, body):
    sock.send(b"HTTP/1.1 " + status.encode('ascii') + CRLF)
    headers.append(('Content-Length', str(len(body))))
    headers.append(('Connection', 'close'))
    header_items = ["{}: {}".format(k, v) for k, v in headers]
    header_bytes = b"".join(h.encode('ascii') + CRLF for h in header_items)
    sock.send(header_bytes)
    sock.send(CRLF)
    sock.send(body)
    sock.close()
