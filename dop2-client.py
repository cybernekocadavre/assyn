#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import socket
import os

# Define port pool range
PORT_POOL_START = 65500
PORT_POOL_END = 65510
current_port_index = PORT_POOL_START

# Function to get the next available port from the pool
def get_next_port():
    global current_port_index
    port = current_port_index
    current_port_index += 1
    if current_port_index > PORT_POOL_END:
        current_port_index = PORT_POOL_START
    return port

def save_key_to_file(filename, key):
    with open(filename, 'w') as file:
        file.write(str(key))

def load_key_from_file(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return int(file.read())
    return None

def main():
    HOST = '127.0.0.1'  # Server IP address
    PORT_ENCRYPTION = 65432  # Port for encryption negotiation
    PORT_COMMUNICATION = 65433  # Port for main communication

    # Socket for encryption negotiation
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_encrypt:
        s_encrypt.connect((HOST, PORT_ENCRYPTION))

        # Receive shared prime and base for encryption negotiation
        shared_prime = int(s_encrypt.recv(1024).decode('utf-8'))
        shared_base = int(s_encrypt.recv(1024).decode('utf-8'))

        # Load or generate client secret for encryption
        client_secret = load_key_from_file('client_secret.txt')
        if client_secret is None:
            client_secret = int(input("Enter your secret key: "))
            save_key_to_file('client_secret.txt', client_secret)

        # Generate and save client's public key for encryption
        client_public_key = (shared_base ** client_secret) % shared_prime
        save_key_to_file('client_public_key.txt', client_public_key)

        # Send client's public key for encryption negotiation
        s_encrypt.sendall(bytes(str(client_public_key), 'utf-8'))

        # Receive server's public key for encryption negotiation
        server_public_key = int(s_encrypt.recv(1024).decode('utf-8'))

        # Calculate shared secret for encryption
        shared_secret = (server_public_key ** client_secret) % shared_prime

        print("Shared secret for encryption:", shared_secret)

    # Socket for main communication
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_communication:
        s_communication.connect((HOST, PORT_COMMUNICATION))

        # Main communication logic goes here

if __name__ == "__main__":
    main()
