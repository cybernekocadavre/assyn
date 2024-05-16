#!/usr/bin/env python
# coding: utf-8

# In[ ]:

# server.py

import socket
from math import sqrt
from secrets import choice
import os

# Function to check if a number is prime
def is_prime(number: int) -> bool:
    if number == 2 or number == 3:
        return True
    elif number % 2 == 0 or number < 2:
        return False
    for current_number in range(3, int(sqrt(number)) + 1, 2):
        if number % current_number == 0:
            return False
    return True

# Function to generate a random prime number within a range
def generate_prime_number(min_value=0, max_value=300):
    primes = [number for number in range(min_value, max_value) if is_prime(number)]
    return choice(primes)

# Function to generate a public key from a base and secret
def generate_public_key(base, secret, prime):
    return (base ** secret) % prime

# Function to calculate the shared secret
def calculate_shared_secret(public_key, secret, prime):
    return (public_key ** secret) % prime

# Function to save a key to a file
def save_key_to_file(filename, key):
    with open(filename, 'w') as file:
        file.write(str(key))

# Function to load a key from a file
def load_key_from_file(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return int(file.read())
    return None

# Main function
def main():
    HOST = '127.0.0.1'  # Server IP address
    PORT = 65432        # Server port number

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        while True:
            conn, addr = s.accept()
            with conn:
                print('Connection established with', addr)

                # Generate shared prime and base
                shared_prime = generate_prime_number()
                shared_base = int(choice(range(2, 20)))

                # Load or generate server secret
                server_secret = load_key_from_file('server_secret.txt')
                if server_secret is None:
                    server_secret = int(choice(range(2, shared_prime - 1)))
                    save_key_to_file('server_secret.txt', server_secret)

                # Send shared prime and base to client
                conn.sendall(bytes(str(shared_prime), 'utf-8'))
                conn.sendall(bytes(str(shared_base), 'utf-8'))

                # Receive client's public key
                client_public_key = int(conn.recv(1024).decode('utf-8'))

                # Load allowed public keys
                allowed_keys = ['client_public_key.txt'] 

                if any(client_public_key == load_key_from_file(key_file) for key_file in allowed_keys):
                    print("Client's public key is valid. Connection accepted.")
                    # Generate and save server's public key
                    server_public_key = generate_public_key(shared_base, server_secret, shared_prime)
                    save_key_to_file('server_public_key.txt', server_public_key)
                    # Send server's public key to client
                    conn.sendall(bytes(str(server_public_key), 'utf-8'))
                    # Calculate shared secret
                    shared_secret = calculate_shared_secret(client_public_key, server_secret, shared_prime)
                    print("Shared secret calculated:", shared_secret)
                    # Save exchange details
                    save_exchange(shared_prime, shared_base, server_secret, 0, server_public_key, 0, shared_secret, 0)
                else:
                    print("Client's public key is not valid. Connection terminated.")

if __name__ == "__main__":
    main()

