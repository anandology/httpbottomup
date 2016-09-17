"""Hello World HTTP Server, written using pure sockets.
"""
import httpserver

def handle_request(method, path, headers):
    return "200 OK", [("Content-type", "text/plain")], b'Hello World!\n'

if __name__ == '__main__':
    httpserver.start_server('localhost', 8080, handle_request)