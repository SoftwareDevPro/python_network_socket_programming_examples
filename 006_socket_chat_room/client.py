
import socket, select, errno, sys

HEADER_LENGTH = 20
IP = "localhost"
PORT = 22333
my_username = input("Username: ")

# Create a socket, connect to it, and set the blocking value
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

# Setup the username and header and send them
uname = my_username.encode('utf-8')
user_header = f"{len(uname):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(user_header + uname)

while True:

    # Wait for user to input a message
    msg = input(f'{my_username} > ')

    if msg:

        # Encode message to bytes, then send it
        msg = msg.encode('utf-8')
        msg_header = f"{len(msg):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(msg_header + msg)

    try:
        # Loop over received messages
        while True:

            user_header = client_socket.recv(HEADER_LENGTH)

            # Server gracefully closed a connection
            if not len(user_header):
                print('Connection closed by the server')
                sys.exit()

            uname_length = int(user_header.decode('utf-8').strip())

            # Receive and decode username
            uname = client_socket.recv(uname_length).decode('utf-8')

            # Read in the actual message
            msg_header = client_socket.recv(HEADER_LENGTH)
            msg_length = int(msg_header.decode('utf-8').strip())
            msg = client_socket.recv(msg_length).decode('utf-8')

            print(f'{uname} > {msg}')

    except IOError as ioe:
        # This happens on non-blocking connections
        if ioe.errno != errno.EAGAIN and ioe.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(ioe)))
            sys.exit()

        continue

    except Exception as exc:
        print('Reading error: '.format(str(exc)))
        sys.exit()

        