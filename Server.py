import socket
import threading

# Server settings
HOST = '127.0.0.1'  # Server IP Address
PORT = 6606        # Port number

# Creating server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

# Dictionary to store connections and usernames
clients = {}

# Sending messages to clients
def send_message(client_socket, message):
    try:
        client_socket.send(message.encode())
    except Exception as e:
        print(f'Error: {str(e)}')

# Function to broadcast messages to clients
def broadcast_message(sender_socket, message):
    for client_socket in clients:
        if client_socket != sender_socket:
            send_message(client_socket, message)

# Function to receive server messages
def receive_server_messages():
    while True:
        message = input('Server: ')
        broadcast_message(None, f'Server: {message}')

# Client processing function
def handle_client(client_socket):
    try:
        # Get username from client
        username = client_socket.recv(1024).decode()
        print(f'{username} connected.')
        send_message(client_socket, 'Connection established. You can start chatting.')

        # Join notification to other clients
        broadcast_message(client_socket, f'{username} joined the chat.')

        # Receiving messages from the client and forwarding them to other clients
        while True:
            message = client_socket.recv(1024).decode()
            if message == 'q':
                # Client leaves the chat
                break
            
            # Print received message on the server
            print(message)
            
            # Send the message without repeating the username
            broadcast_message(client_socket, message)
    except Exception as e:
        print(f'Error: {str(e)}')
    finally:
        # Close client connection
        client_socket.close()
        del clients[client_socket]
        broadcast_message(None, f'{username} left the chat.')

# Start receiving server messages
server_receive_thread = threading.Thread(target=receive_server_messages)
server_receive_thread.start()

# Listening to the server
print('Chat server started...')
while True:
    client_socket, client_address = server_socket.accept()
    # Accepting client connection
    clients[client_socket] = client_address
    client_socket.send('Enter your username: '.encode())
    threading.Thread(target=handle_client, args=(client_socket,)).start()
