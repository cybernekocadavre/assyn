#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import asyncio
import socket

async def main():
    # Конфигурация клиента
    HOST = '127.0.0.1'  # IP-адрес сервера
    PORT = 65432        # Порт, используемый сервером

    # Установка соединения через сокет
    reader, writer = await asyncio.open_connection(HOST, PORT)

    # Получение общего простого числа и базы от сервера
    shared_prime = int((await reader.read(1024)).decode())
    shared_base = int((await reader.read(1024)).decode())

    # Генерация секрета клиента
    client_secret = int(input("Введите ваш секретный ключ: "))

    # Генерация открытого ключа клиента
    client_public_key = (shared_base ** client_secret) % shared_prime

    # Отправка открытого ключа клиента серверу
    writer.write(str(client_public_key).encode())

    # Получение открытого ключа сервера
    server_public_key = int((await reader.read(1024)).decode())

    # Вычисление общего секрета
    shared_secret = (server_public_key ** client_secret) % shared_prime

    print("Общий секрет вычислен:", shared_secret)

    # Закрытие соединения
    writer.close()
    await writer.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
