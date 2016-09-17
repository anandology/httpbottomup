"""WSGI ADD server.
"""

from wwf import application, set_mapping

def render_home(request):
    return [b'A form will come here']

def render_add(request):
    q = request.query
    x = int(q['x'])
    y = int(q['y'])
    z = x+y
    msg = "Result is {}".format(z)
    return [msg.encode('ascii')]

urls = [
    ("/", render_home),
    ("/add", render_add)
]
set_mapping(urls)

