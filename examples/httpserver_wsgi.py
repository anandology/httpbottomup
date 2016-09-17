"""Simple WSGI Server Library.

USAGE:

    # hello.py
    def application(environ, start_response):
        start_response("200 OK", [("Content-type": "text/plain")])
        return [b'Hello World!']

Run it using:

    $ python httpserver_wsgi.py hello:application

"""
import sys
import os
from socket import *

CRLF = b"\r\n"

def start_server(host, port, application):            
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(5)

    print("Started server on http://{}:{}/".format(host, port))

    with sock:
        while True:
            client, addr = sock.accept()
            handle_request(client, addr, application)

def handle_request(client, addr, application):
    def start_response(status, headers):
        write_headers(client, status, headers)

    method, path, req_headers = read_request(client)
    env = make_environ(method, path, req_headers)

    data = application(env, start_response)

    for chunk in data:
        client.send(chunk)
    client.close()

def make_environ(method, path, headers):
    env = {
        'REQUEST_METHOD': method,
        'RAW_URI': path
    }

    if "?" in path:
        path, qs = path.split("?", 1)
    else:
        qs = ""
    env["PATH_INFO"] = path
    env["QUERY_STRING"] = qs
    
    for name, value in headers.items():
        key = "HTTP_" + name.upper().replace("-", "_")
        env[key] = value

    return env
    

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

def write_headers(sock, status, headers):
    sock.send(b"HTTP/1.1 " + status.encode('ascii') + CRLF)
    #headers.append(('Content-Length', str(len(body))))
    headers.append(('Connection', 'close'))
    header_items = ["{}: {}".format(k, v) for k, v in headers]
    header_bytes = b"".join(h.encode('ascii') + CRLF for h in header_items)
    sock.send(header_bytes)
    sock.send(CRLF)

def main():
    modname = sys.argv[1]
    if ":" in modname:
        modname, funcname = modname.split(":", 1)
    else:
        funcname = 'application'
    module = __import__(modname)
    app = getattr(module, funcname)
    
    start_server('localhost', 8000, app)


if __name__ == "__main__":
    main()
