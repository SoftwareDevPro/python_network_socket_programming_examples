
import socket

HEADERSIZE = 5

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((socket.gethostname(), 3599))

while True:
    full_message = ''
    new_message = True
    while True:
        msg = sock.recv(16)
        if new_message:
            print("new message length:",msg[:HEADERSIZE])
            msglen = int(msg[:HEADERSIZE])
            new_message = False

        print(f"full message length: {msglen}")

        full_message += msg.decode("utf-8")
        print(len(full_message))

        if len(full_message) - HEADERSIZE == msglen:
            print(f"full message received:[{full_message[HEADERSIZE:]}]")
            #print()
            new_message = True
            full_message = ""