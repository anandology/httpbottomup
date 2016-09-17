"""wwf - weird web framework - v1

Uses global state for managing all the application data.
"""

_mapping = []
request = None

class Request:
    def __init__(self, environ):
        self.environ = environ
        self.path = environ['PATH_INFO']
        self.method = environ['REQUEST_METHOD']
        self.query = self.parse_qs(environ['QUERY_STRING'])

    def parse_qs(self, qs):
        # This assumes that there is no duplicates in query string.
        parts = qs.split("&")
        pairs = [part.split("=", 1) for part in parts]
        return dict(pairs)

def set_mapping(mapping):
    """Initializes the URL mapping.

    mapping should be a list if tuples. 

    set_mapping([("/", home_page), 
                 ("/login", login_page)])
    """
    global _mapping
    _mapping = mapping

def application(environ, start_response):      
    global request
    request = Request(environ)

    # FIX ME:
    start_response("200 OK", [("Content-type", "text/html")])
    
    path = environ['PATH_INFO']
    for path2, func in _mapping:
        if path == path2:
            return func(request)
    return notfound()

def notfound():
    return b'Not Found'
    
