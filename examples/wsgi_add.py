"""WSGI ADD server.
"""

def application(environ, start_response):
    path = environ['PATH_INFO']
    if path == "/":
        start_response("200 OK", [("Content-Type", "text/html")])
        return render_home(environ)
    elif path == "/add":
        start_response("200 OK", [("Content-Type", "text/html")])
        return render_add(environ)
    else:
        start_response("404 Not Found", [("Content-Type", "text/html")])
        return []

def render_home(environ):
    return [b'A form will come here']

def render_add(environ):
    return [b'The result is 42']
