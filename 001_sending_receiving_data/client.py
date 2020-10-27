
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((socket.gethostname(), 6789))

while True:
    complete_message = ''

    while True:
        msg = sock.recv(8)
        
        if len(msg) <= 0:
            break
        
        complete_message += msg.decode("utf-16")

    if len(complete_message) > 0:
        print(complete_message)
