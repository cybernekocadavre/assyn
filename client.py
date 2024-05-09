#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import socket

def main():
    host = '127.0.0.1'
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    prime = int(client_socket.recv(1024).decode())
    client_socket.sendall(b"ACK")  # Send acknowledgment to server

    base = int(client_socket.recv(1024).decode())
    client_socket.sendall(b"ACK")  # Send acknowledgment to server

    client_public_key = int(client_socket.recv(1024).decode())
    client_socket.sendall(b"ACK")  # Send acknowledgment to server

    private_key = int(input("Enter private key: "))
    public_key = (base ** private_key) % prime

    client_socket.sendall(str(public_key).encode())
    client_socket.recv(1024)  # Wait for acknowledgment from server

    shared_secret = (int(client_socket.recv(1024).decode()) ** private_key) % prime
    print("Shared secret:", shared_secret)

    client_socket.close()

if __name__ == "__main__":
    main()


