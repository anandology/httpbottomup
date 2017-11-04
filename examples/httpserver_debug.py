"""HTTP Server Explorer.
"""
import httpserver

def handle_request(method, path, headers):
    body = method + " " + path + "\n\n" + "HEADERS:\n\n"
    for name, value in headers.items():
        body += "{}: {}\n".format(name, value)

    return "200 OK", [("Content-type", "text/plain")], body.encode("ascii")

if __name__ == '__main__':
    httpserver.start_server('localhost', 8080, handle_request)