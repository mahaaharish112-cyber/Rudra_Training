import socket

HOST = "127.0.0.1"
PORT = 5000

OUTPUT = "image_received.png"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((HOST, PORT))

print("Connected to server")

file_size = int(client.recv(1024).decode())

print("Image size:", file_size, "bytes")

client.send(b"READY")

received = 0

with open(OUTPUT, "wb") as file:
    while received < file_size:
        data = client.recv(4096)

        if not data:
            break

        file.write(data)

        received += len(data)

print("Image received successfully")

client.close()
