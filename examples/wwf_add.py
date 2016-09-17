"""WSGI ADD server.
"""
import wwf

def render_home():
    return open("../data/add.html").read()

def render_add():
    cookies = wwf.cookies()
    count = int(cookies.get("counter", 0)) + 1
    wwf.setcookie("counter", str(count))

    q = wwf.query()
    if 'x' not in q or 'y' not in q:
        wwf.set_status("404 Bad Data")
        return "Bad Data"
    x = int(q['x'])
    y = int(q['y'])
    z = x+y
    wwf.add_header("Content-type", "text/plain")
    msg = "Result is {}\nCalled {} times.".format(z, count)
    return msg

urls = [
    ("/", render_home),
    ("/add", render_add)
]
wwf.set_mapping(urls)

application = wwf.application

