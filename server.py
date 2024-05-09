#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import socket
from math import sqrt
from secrets import choice

def is_prime(number: int) -> bool:
    """Checks if the provided value is a prime number."""
    if number == 2 or number == 3:
        return True
    elif number % 2 == 0 or number < 2:
        return False
    for current_number in range(3, int(sqrt(number)) + 1, 2):
        if number % current_number == 0:
            return False
    return True

def generate_prime_number(min_value=0, max_value=300):
    """Generates a random prime number within the specified range."""
    primes = [number for number in range(min_value, max_value) if is_prime(number)]
    return choice(primes)

def generate_public_key(base, secret, prime):
    """Generates public key."""
    return (base ** secret) % prime

def calculate_shared_secret(public_key, secret, prime):
    """Calculates the shared secret."""
    return (public_key ** secret) % prime

def save_exchange(p, g, a, b, A, B, a_s, b_s, path="exchange.txt"):
    """Saves the exchange details to a file."""
    exchange = "Begin of exchange\n\n"
    exchange += f"First a shared prime (p) & shared base (g) were generated:\n\tp = {p}\n\tg = {g}\n\n"
    exchange += f"Next Alice and Bob generated their own private secrets (a and b respectively):\n\ta = {a}\n\tb = {b}\n\n"
    exchange += f"Alice and Bob now compute their public secrets and send them to each other. \nThese are represented as A and B respectively:\n\tA = g^a mod p = {A}\n\tB = g^b mod p = {B}\n\n"
    exchange += f"Alice and Bob can now calculate a common secret that can be used to encrypt later transmissions:\n\tAlice's Calculation:\n\t\ts = B^a mod p = {a_s} \n\tBob's Calculation:\n\t\ts = A^b mod p = {b_s}"

    with open(path, "w+") as output_file:
        output_file.write(exchange)

    return exchange

def main():
    # Server configuration
    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

    # Establishing socket connection
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        # Accepting incoming connection
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)

            # Generating shared prime and base
            shared_prime = generate_prime_number()
            shared_base =  int(choice(range(2, 20)))  # Choosing a random base for simplicity

            # Generating server's private secret
            server_secret = int(choice(range(2, shared_prime - 1)))

            # Sending shared prime and base to client
            conn.sendall(bytes(str(shared_prime), 'utf-8'))
            conn.sendall(bytes(str(shared_base), 'utf-8'))

            # Receiving client's public key
            client_public_key = int(conn.recv(1024).decode('utf-8'))

            # Generating server's public key
            server_public_key = generate_public_key(shared_base, server_secret, shared_prime)

            # Sending server's public key to client
            conn.sendall(bytes(str(server_public_key), 'utf-8'))

            # Calculating shared secret
            shared_secret = calculate_shared_secret(client_public_key, server_secret, shared_prime)

            # Saving exchange details
            save_exchange(shared_prime, shared_base, server_secret, 0, server_public_key, 0, shared_secret, 0)

            print("Shared secret calculated:", shared_secret)

if __name__ == "__main__":
    main()


