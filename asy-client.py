#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import asyncio

async def main():
    # Configuration
    HOST = '127.0.0.1'
    PORT = 65432

    # Establish connection
    reader, writer = await asyncio.open_connection(HOST, PORT)

    # Receive shared prime and base from the server
    shared_prime = int(await reader.readline())
    shared_base = int(await reader.readline())

    # Get the secret key from the user
    client_secret = input("Enter your secret key: ")

    # Generate client's public key
    client_public_key = (shared_base ** int(client_secret)) % shared_prime

    # Send client's public key to the server
    writer.write(f"{client_public_key}\n".encode())
    await writer.drain()

    # Receive server's public key
    server_public_key = int(await reader.readline())

    # Compute shared secret
    shared_secret = (server_public_key ** int(client_secret)) % shared_prime

    print("Shared secret computed:", shared_secret)

    # Close the connection
    writer.close()
    await writer.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())



