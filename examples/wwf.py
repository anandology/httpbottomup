"""wwf - weird web framework - v1

Uses global state for managing all the application data.
"""

_mapping = []
request = None

_status = "200 OK"
_headers = []

class Request:
    def __init__(self, environ):
        self.environ = environ
        self.path = environ['PATH_INFO']
        self.method = environ['REQUEST_METHOD']
        self.query = self.parse_qs(environ['QUERY_STRING'])
        self.headers = self.read_headers(environ)

    def parse_qs(self, qs):
        # This assumes that there is no duplicates in query string.
        parts = qs.split("&")
        pairs = [part.split("=", 1) for part in parts if "=" in part]
        return dict(pairs)

    def read_headers(self, environ):
        headers = {}
        for k, v in environ.items():
            if k.startswith("HTTP_"):
                name = k[len("HTTP_"):].replace("_", "-").lower()
                headers[name] = v
        return headers

def set_mapping(mapping):
    """Initializes the URL mapping.

    mapping should be a list if tuples. 

    set_mapping([("/", home_page), 
                 ("/login", login_page)])
    """
    global _mapping
    _mapping = mapping

def application(environ, start_response):      
    global request, _status, _headers
    request = Request(environ)
    _status = "200 OK"
    _headers = []

    response = handle_request()
    start_response(_status, _headers)
    return [response.encode('ascii')]
    
def handle_request():
    for path, func in _mapping:
        if path == request.path:
            return func()
    set_status("404 Not Found")
    return notfound()

def query():
    return request.query

def get_header(name):
    """Returns a request header.
    """
    return request.headers[name]

def set_status(status):
    global _status
    _status = status

def add_header(name, value):
    _headers.append((name, value))
    
def notfound():
    return b'Not Found'
    
def cookies():
    """Returns the cookies as a dictionary.
    """
    cookie_str = request.headers.get("cookie", "")
    parts = cookie_str.split(";")
    pairs = [part.strip().split("=", 1) for part in parts if "=" in part]
    return dict(pairs)

def setcookie(name, value):
    add_header("Set-Cookie", "{}={}".format(name, value))
