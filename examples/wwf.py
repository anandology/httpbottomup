"""wwf - weird web framework - v1

Uses global state for managing all the application data.
"""

_mapping = []

def set_mapping(mapping):
    """Initializes the URL mapping.

    mapping should be a list if tuples. 

    set_mapping([("/", home_page), 
                 ("/login", login_page)])
    """
    global _mapping
    _mapping = mapping

def application(environ, start_response):      
    # FIX ME:
    start_response("200 OK", [("Content-type", "text/html")])
    
    path = environ['PATH_INFO']
    for path2, func in _mapping:
        if path == path2:
            return func()
    return notfound()

def notfound():
    return b'Not Found'
    
