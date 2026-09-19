import socket
import threading

HOST = "127.0.0.1"
PORT = 5000


def receive_messages(client):
    while True:
        try:
            message = client.recv(1024).decode()

            if not message:
                break

            print(f"\nServer: {message}")
            print("You: ", end="", flush=True)

        except:
            break


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((HOST, PORT))

print("Connected to server")

thread = threading.Thread(
    target=receive_messages,
    args=(client,)
)

thread.start()

while True:
    message = input("You: ")

    if message.lower() == "exit":
        client.send("exit".encode())
        break

    client.send(message.encode())

client.close()
