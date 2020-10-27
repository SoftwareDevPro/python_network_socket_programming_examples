
import socket, pickle

HEADERSIZE = 5

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((socket.gethostname(), 38901))

while True:
    
    full_message = b''
    new_message = True
    while True:

        message = sock.recv(32)
        
        if new_message:
            print("new msg len:", message[:HEADERSIZE])
            msglen = int(message[:HEADERSIZE])
            new_message = False

        print(f"full message length: {msglen}")

        full_message += message

        print(len(full_message))

        if len(full_message) - HEADERSIZE == msglen:
            print("full msg recvd")
            print(full_message[HEADERSIZE:])
            print(pickle.loads(full_message[HEADERSIZE:]))
            new_message = True
            full_message = b""

            