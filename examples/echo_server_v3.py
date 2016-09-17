import socket
import sys
from threading import Thread

def echo_server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(5)
    
    while True:
        print("waiting to accept connections on", host, port) 
        client_sock, client_addr = sock.accept()
        #handle_client(client_sock, client_addr)
        t = Thread(target=handle_client, args=(client_sock, client_addr))
        t.start()

def handle_client(client_sock, client_addr):
    print("New connection from", client_addr)
    host, port = client_addr

    rfile = client_sock.makefile("r")
    wfile = client_sock.makefile("w")

    msg = "Hello {}:{}\n".format(host, port)
    wfile.write(msg)

    while True:
        message = rfile.readline()
        if not message:
            break
        wfile.write(message)
        wfile.flush()

    client_sock.close()
    wfile.close()
    rfile.close()

def main():
    port = int(sys.argv[1])
    echo_server('localhost', port)

if __name__ == "__main__":
    main()
