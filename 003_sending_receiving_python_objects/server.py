
import socket, time, pickle

HEADERSIZE = 5

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((socket.gethostname(), 38901))

sock.listen(10)

while True:
    clientsocket, address = sock.accept()
    print(f"Connection with {address} established");

    obj = { 1:"hello", 2: "world" }
    
    msg = pickle.dumps(obj)
    msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8') + msg
    
    print(msg)
    
    clientsocket.send(msg)

    