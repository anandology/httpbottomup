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

def handle_request(sock, remote_addr):
    fileobj = sock.makefile('r')

    status_line = fileobj.readline()
    method, path, protocol = status_line.strip().split()

    # Path starts with /. Remove that to make a path in the file system
    filepath = "." + path

    status = "200 OK"
    headers = [
        "Server: Simple HTTP Server",
        "Connection: Close",
        "Content-type: text/html"
    ]
    body = b""


    if not os.path.exists(filepath):
        status = "404 Not Found"
    elif os.path.isdir(filepath) and not filepath.endswith("/"):
        status = '302 Found'
        headers.append('Location: {}/'.format(path))
    elif os.path.isdir(filepath):
        body = list_directory(filepath).encode('ascii')
    else:
        body = open(filepath, 'rb').read()

    headers.append("Content-Length: {}".format(len(body)))

    sock.send(b"HTTP/1.1 " + status.encode('ascii') + CRLF)
    header_bytes = b"".join(h.encode('ascii') + CRLF for h in headers)
    sock.send(header_bytes)
    sock.send(CRLF)
    sock.send(body)
    sock.close()

def list_directory(path):
    files = os.listdir(path)
    return "".join('<a href="{}">{}</a><br>\n'.format(f, f) for f in files)    

def main():
    host = sys.argv[1]
    port = int(sys.argv[2])
    http_server(host, port)

if __name__ == '__main__':
        main()