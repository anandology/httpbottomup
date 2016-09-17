"""WSGI ADD server.
"""

from wwf import application, set_mapping

def render_home():
    return [b'A form will come here']

def render_add():
    return [b'The result is 42']

urls = [
    ("/", render_home),
    ("/add", render_add)
]
set_mapping(urls)

