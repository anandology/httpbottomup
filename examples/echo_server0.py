import socket
import sys

def echo_server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(1)
    
    print("listening on", host, port) 
    client_sock, client_addr = sock.accept()
    handle_client(client_sock, client_addr)

def handle_client(client_sock, client_addr):
    print("New connection from", client_addr)
    host, port = client_addr
    msg = "Hello {}:{}\n".format(host, port)
    client_sock.send(msg.encode('ascii'))
    
    message = client_sock.recv(1024)
    client_sock.send(message)

    client_sock.close()

def main():
    try:
        port = int(sys.argv[1])
    except IOError:
        port = 8000
    echo_server('localhost', port)

if __name__ == "__main__":
    main()
