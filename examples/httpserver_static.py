"""HTTP Server to serve static files.
"""
import httpserver
import os.path

def handle_request(method, path, headers):
    document_root = "."
    filepath = document_root + path
    print(filepath)
    if os.path.isfile(filepath):
        ctype = find_content_type(filepath)
        body = open(filepath, 'rb').read()
        return "200 OK", [("Content-type", ctype)], body
    else:
        body = b"The file you have required is not found.\n"
        return "404 Not Found", [("Content-type", "text/html")], body
        
def find_content_type(filepath):
    ext = filepath.split(".")[-1]
    ctypes = {
        "html": "text/html",
        "png": "image/png",
        "jpg": "image/jpeg",
        "txt": "text/plain",
        "py": "text/plain",
    }
    return ctypes.get(ext, "application/octet-stream")

if __name__ == '__main__':
    httpserver.start_server('localhost', 8080, handle_request)
