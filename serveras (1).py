#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import socket
import random

def generate_prime():
    primes = [i for i in range(2, 100) if all(i % j != 0 for j in range(2, i))]
    return random.choice(primes)

def calculate_public_key(base, private_key, prime):
    return (base ** private_key) % prime

def calculate_shared_secret(public_key, private_key, prime):
    return (public_key ** private_key) % prime

def main():
    host = '127.0.0.1'
    port = 12345

    prime = generate_prime()
    base = random.randint(2, prime - 1)

    private_key = random.randint(2, prime - 1)
    public_key = calculate_public_key(base, private_key, prime)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print("Server is listening...")

    conn, addr = server_socket.accept()
    print("Connection from:", addr)

    conn.sendall(str(prime).encode())
    conn.recv(1024)

    conn.sendall(str(base).encode())
    conn.recv(1024)

    conn.sendall(str(public_key).encode())
    client_public_key = int(conn.recv(1024).decode())

    shared_secret = calculate_shared_secret(client_public_key, private_key, prime)
    print("Shared secret:", shared_secret)

    conn.close()

if __name__ == "__main__":
    main()

