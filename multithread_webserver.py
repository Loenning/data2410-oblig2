#imports
from socket import *
import _thread as thread
import sys
import time

# function which returns the current time
def now():
    return time.ctime(time.time())  # Get the current time in human-readable format

# function for handling client connections
def handleClient(connectionSocket):
    try:
        time.sleep(3)  # Simulate a delay before processing the request (3 seconds)

        message = connectionSocket.recv(1024).decode()  # Receive a message from the client (up to 1024 bytes)

        if not message:  # If no message is received (client disconnected), close the connection
            connectionSocket.close()
            return

        filename = message.split()[1]  # Extract the requested file from the HTTP request

        try:
            # Try to open the requested file (excluding the first character, '/')
            f = open(filename[1:])
            outputdata = f.read()  # Read the content of the file

            # Send HTTP response header with status code 200 OK
            connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
            connectionSocket.send("Content-Type: text/html\r\n\r\n".encode())

            # Send the file content to the client in chunks (one character at a time)
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i].encode())
            connectionSocket.send("\r\n".encode())  # Send a final carriage return and newline

        except FileNotFoundError:  # If the requested file is not found, send a 404 error
            connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())
            connectionSocket.send("Content-Type: text/html\r\n\r\n".encode())
            connectionSocket.send("<html><body><h1>404 Not Found</h1></body></html>".encode())

    except Exception as e:  # Handle any unexpected errors during the process
        print(f"Error handling client: {e}")

    finally:
        connectionSocket.close()  # Close the connection to the client

# Main function to set up and run the server
def main():

    serverSocket = socket(AF_INET, SOCK_STREAM)  # Create a socket for the server (IPv4, TCP)

    port = 8000  # Define the port number to listen on
    server_ip = '127.0.0.1'  # Define the server IP (localhost)

    try:
        serverSocket.bind((server_ip, port))  # Bind the socket to the server's IP address and port
    except:
        print("Failed to bind. Error : ")  # Print an error if binding fails
        sys.exit()  # Exit the program if binding fails

    serverSocket.listen(5)  # Start listening for incoming connections (maximum of 5 pending connections)
    print('Server is ready to receive connections...')  # Print a message indicating the server is ready

    connection_count = 0  # Initialize a counter for the number of connections

    while True:
        # Accept an incoming connection
        connectionSocket, addr = serverSocket.accept()
        print(f"Connection from {addr}")  # Print the client's IP address and port
        print(f"at ", now())  # Print the current time

        # Start a new thread to handle the client request
        thread.start_new_thread(handleClient, (connectionSocket,))

        connection_count += 1  # Increment the connection counter

    #serverSocket.close()  # Close the server socket (this code is currently unreachable)
    #sys.exit()  # Terminate the program after sending the corresponding data (this code is also unreachable)

# Check if the script is being run directly (not imported)
if __name__ == '__main__':
    main()  # Call the main function to start the server
