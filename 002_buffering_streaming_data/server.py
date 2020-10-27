
import socket
import time

HEADERSIZE = 5

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((socket.gethostname(), 3599))
sock.listen(5)

while True:

    clientsocket, address = sock.accept()
    print(f"Connection established with {address}.")

    message = "Hello World"
    message = f"{len(message):<{HEADERSIZE}}" + message

    print(f"message := {message}")

    clientsocket.send(bytes(message, "utf-8"))

    while True:

        time.sleep(4)
        
        message = f"The time is {time.ctime()}"
        message = f"{len(message):<{HEADERSIZE}}"+message

        print(message)

        clientsocket.send(bytes(message,"utf-8"))