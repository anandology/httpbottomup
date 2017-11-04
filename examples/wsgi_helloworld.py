"""Simple Hello world WSGI app.

Run this using gunicorn.

    gunicorn wsgi_helloworld:application

You'll have to install gunicorn first. Install it using:

    pip install gunicorn    
"""

def application(environ, start_response):
    """Simple Hello World WSGI app.
    """
    start_response("200 OK", [("Content-Type", "text/plain")])
    return [b"Hello World\n"]

if __name__ == "__main__":
    from httpserver_wsgi import start_server
    start_server("localhost", 8000, application)
