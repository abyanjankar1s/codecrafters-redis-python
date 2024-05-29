import socket
import threading

def redis(command):
    cmd = command.decode("utf-8")
    if "PING" in cmd:
        return b"+PONG\r\n"
    return b""

def handle_client(connection, address):
    while True:
        try:
            # Read data
            data = connection.recv(512)
            if not data:
                print(f"Connection from {address} closed.")
                return
            # Write the same data back
            connection.sendall(redis(data))
        except ConnectionResetError:
            print(f"Connection from {address} reset.")
            return

def main():
    print("Logs from your program will appear here!")
    with socket.create_server(("localhost", 6379), reuse_port=True) as server_socket:
        while True:
            # Wait for client
            connection, address = server_socket.accept()
            print(f"Accepted connection from {address}")
            client_thread = threading.Thread(
                target=handle_client, args=(connection, address)
            )
            client_thread.start()

if __name__ == "__main__":
    main()
