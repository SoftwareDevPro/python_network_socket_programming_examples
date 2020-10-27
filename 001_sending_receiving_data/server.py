
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind((socket.gethostname(), 6789))
sock.listen(5)

while True:
    clientsocket, address = sock.accept()
    print(f"Connection established with {address}.")
    clientsocket.send(bytes("Hello World","utf-16"))
    clientsocket.close()