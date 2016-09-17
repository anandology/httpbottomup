import sys
from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM
import threading

def main():
    host = sys.argv[1]
    port = int(sys.argv[2])

    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(10)
    while True:
        client, addr = sock.accept()
        t = threading.Thread(target=handle_conn, args=(client, addr))
        t.start()

def handle_conn(client, addr):
    while True:
        x = client.read()
        if not x:
            break
        client.send(x)
    client.close()

if __name__ == '__main__':
    main()


