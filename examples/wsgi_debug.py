"""WSGI app to print the environ.

USAGE:

	gunicorn wsgi_debug:application
"""
import pprint

def application(environ, start_response):
    """WSGI app to show the env.
    """
    start_response("200 OK", [("Content-Type", "text/plain")])
    env_text = pprint.pformat(environ, indent=4)
    return [env_text.encode('ascii')]
