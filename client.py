#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import socket

def main():
    # Client configuration
    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 65432        # The port used by the server

    # Establishing socket connection
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        # Receiving shared prime and base from server
        shared_prime = int(s.recv(1024).decode('utf-8'))
        shared_base = int(s.recv(1024).decode('utf-8'))

        # Generating client's private secret
        client_secret = int(input("Enter your private secret: "))

        # Generating client's public key
        client_public_key = (shared_base ** client_secret) % shared_prime

        # Sending client's public key to server
        s.sendall(bytes(str(client_public_key), 'utf-8'))

        # Receiving server's public key
        server_public_key = int(s.recv(1024).decode('utf-8'))

        # Calculating shared secret
        shared_secret = (server_public_key ** client_secret) % shared_prime

        print("Shared secret calculated:", shared_secret)

if __name__ == "__main__":
    main()



