#Uncomment this to pass the first stage
import socket
import threading


def ping_client(client_socket):
    client_socket.send(b"+PONG\r\n")

def handle_connection(conn, addr):
    while True:
        request: bytes = conn.recv(1024)
        if not request:
            break
        data: str = request.decode()
        if "ping" in data.lower():
            response = "+PONG\r\n"
            conn.send(response.encode())
    conn.close()


def main():
    print("Logs from your program will appear here!")
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    client_conn, addr = server_socket.accept() # wait for client
    while True:
        if client_conn:
            data = client_conn.recv(1024)
            if not data:
                break
            client_conn.sendall(b"+PONG\r\n")
        client_conn, addr = server_socket.accept() 
        print(f"Received connection {client_conn}")
        threading.Thread(target=handle_connection, args=[client_conn, addr])


if __name__ == "__main__":
    main()