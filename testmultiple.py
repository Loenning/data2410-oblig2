# client.py
import socket
import threading
import time

def client_request():
    server_ip = '127.0.0.1'
    port = 8000
    message = "GET /index.html HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n"

    # Create a socket to connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, port))

    # Send a GET request to the server
    client_socket.send(message.encode())

    # Receive the server response
    response = client_socket.recv(1024).decode()
    print(f"Client received: {response}")

    # Close the client socket
    client_socket.close()

def test_multiple_clients(num_clients=5):
    threads = []
    for _ in range(num_clients):
        client_thread = threading.Thread(target=client_request)
        client_thread.start()
        threads.append(client_thread)

        time.sleep(0.5)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

# Run the test with 10 clients
if __name__ == "__main__":
    test_multiple_clients(5)