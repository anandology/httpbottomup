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
    method, path = read_status_line()
    headers = read_headers()
    return method, path, headers

def read_status_line(sock):
    line = fileobj.readline()
    method, path, protocol = line.strip().split()
    return method, path

def read_headers(sock):
    # assuming there won't be any duplicate headers, storing them in a dictionary
    headers = {}
    while True:
        line = sock.readline().strip()
        if not line:
            break
        name, value = line.split(":")
        headers[name.strip().lower()] = value.strip()
    return headers

def handle_request(sock, remote_addr):
    fileobj = sock.makefile('r')

    status_line = fileobj.readline()
    method, path, request_headers = read_request()

    status = "200 OK"
    headers = [
        "Server: Simple HTTP Server",
        "Connection: Close",
        "Content-type: text/plain"
    ]
    body = b"Hello World\n"

    headers.append("Content-Length: {}".format(len(body)))

    sock.send(b"HTTP/1.1 " + status.encode('ascii') + CRLF)
    header_items = ["{}: {}".format(k, v) for k, v in headers)
    header_bytes = b"".join(h.encode('ascii') + CRLF for h in header_items)
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