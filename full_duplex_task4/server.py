import socket
import threading

HOST = "127.0.0.1"
PORT = 5000


def receive_messages(conn):
    while True:
        try:
            message = conn.recv(1024).decode()

            if not message:
                break

            print(f"\nClient: {message}")
            print("You: ", end="", flush=True)

        except:
            break


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))
server.listen(1)

print("Server started")
print(f"Waiting for connection on {HOST}:{PORT}")

conn, address = server.accept()

print(f"Client connected: {address}")

thread = threading.Thread(
    target=receive_messages,
    args=(conn,)
)

thread.start()

while True:
    message = input("You: ")

    if message.lower() == "exit":
        conn.send("exit".encode())
        break

    conn.send(message.encode())

conn.close()
server.close()
