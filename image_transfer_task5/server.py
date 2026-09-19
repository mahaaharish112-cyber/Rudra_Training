import socket
import os

HOST = "127.0.0.1"
PORT = 5000

IMAGE = "image.png"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))
server.listen(1)

print("Server started")
print("Waiting for client...")

conn, address = server.accept()

print("Client connected:", address)

file_size = os.path.getsize(IMAGE)

conn.send(str(file_size).encode())

conn.recv(1024)

with open(IMAGE, "rb") as file:
    while True:
        data = file.read(4096)

        if not data:
            break

        conn.sendall(data)

print("Image sent successfully")

conn.close()
server.close()
