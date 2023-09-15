import socket
import threading

# Server settings
HOST = '127.0.0.1'  # Server IP Address
PORT = 6606        # Port number

# Creating client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Get the username
username = input('Please enter your username: ')
client_socket.send(username.encode())

# Function to receive messages from the server and display them
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            if message.startswith('Server: '):
                print(message)
            else:
                print(f'{message}')
        except Exception as e:
            print(f'Error: {str(e)}')
            break

# Function to send messages to the server
def send_messages():
    while True:
        message = input()
        if message == 'q':
            break
        client_socket.send(message.encode())

# Start receiving messages from the server
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Start sending messages to the server
send_messages()
