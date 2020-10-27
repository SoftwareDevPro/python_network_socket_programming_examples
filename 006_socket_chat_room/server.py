
import socket, select

HEADER_LENGTH = 20
IP = "localhost"
PORT = 22333

# Create a socket, and set the socket options
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket, and start listening
server_socket.bind((IP, PORT))
server_socket.listen()

# List of sockets for select.select()
sockets_list = [ server_socket ]

# List of connected clients - key: socket, value: user header and name as data
clients = {}

print(f'Listening to {IP}:{PORT}')

# Handles message receiving
def receive_message(client_socket):

    try:
        msg_header = client_socket.recv(HEADER_LENGTH)

        # Received no data
        if not len(msg_header):
            return False

        msg_len = int(msg_header.decode('utf-8').strip())

        return { 'header' : msg_header, 'data' : client_socket.recv(msg_len) }

    except:
        # Connection was closed for some reason
        return False

while True:

    # Get the read/exception sockets (this is a blocking call)
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    # Iterate over notified sockets
    for notified_socket in read_sockets:

        # If notified socket is a server socket - new connection, accept it
        if notified_socket == server_socket:

            client_socket, client_address = server_socket.accept()

            # Client should send his name right away, receive it
            user = receive_message(client_socket)

            # client disconnected before he sent username
            if user is False:
                continue

            # Add accepted socket to select.select() list
            sockets_list.append(client_socket)

            # Also save username and username header
            clients[client_socket] = user

            print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))

        # Existing socket is sending a message
        else:

            msg = receive_message(notified_socket)

            # Client disconnected, cleanup
            if msg is False:
                print('Closed connection: {}'.format(clients[notified_socket]['data'].decode('utf-8')))

                # Remove from list for socket.socket(), and list of users
                sockets_list.remove(notified_socket)
                del clients[notified_socket]

                continue

            # Get user by notified socket, so we will know who sent the message
            user = clients[notified_socket]

            print(f'Received message from {user["data"].decode("utf-8")}: {msg["data"].decode("utf-8")}')

            # Send the message to all the clients
            for client_socket in clients:

                # But don't sent it to sender
                if client_socket != notified_socket:

                    # send out the user and message data
                    out_msg = user['header'] + user['data'] + msg['header'] + msg['data']
                    client_socket.send(out_msg)

    # Remove sockets with exceptions
    for notified_socket in exception_sockets:

        sockets_list.remove(notified_socket)

        del clients[notified_socket]
        