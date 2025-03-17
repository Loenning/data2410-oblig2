#imports
import argparse  # Import argparse to handle command-line arguments
from socket import *  # Import all socket-related functions and constants

# Create a parser object to handle CLI input
parser = argparse.ArgumentParser()

# Add expected command-line arguments
parser.add_argument('-i', '--server_ip', type=str, required=True)  # IP address of the server
parser.add_argument('-p', '--server_port', type=int, required=True)  # Port number of the server
parser.add_argument('-f', '--filename', type=str, required=True)  # The filename to request from the server

# Parse the arguments and assign them to the 'args' variable
args = parser.parse_args()

# Create variables based on the parsed argument values
server_ip = args.server_ip  # Server's IP address
server_port = args.server_port  # Server's port number
filename = args.filename  # The requested filename

# Set up the client socket using IPv4 and TCP protocol
clientSocket = socket(AF_INET, SOCK_STREAM)

try:
    # Attempt to connect the client socket to the server at the specified IP and port
    clientSocket.connect((server_ip, server_port))
    print(f"Connected to {server_ip} on port {server_port} using file {filename}")

    # Construct the GET request string with the provided filename, server IP, and port
    get_request = f"GET /{filename} HTTP/1.1\r\nHost: {server_ip}:{server_port}\r\nConnection: close\r\n\r\n"
    print("GET request: ", get_request)

    # Send the GET request to the server
    clientSocket.send(get_request.encode())

    # Initialize an empty byte variable to store the server's response
    response = b""

    # Loop to receive data from the server in chunks
    while True:
        chunk = clientSocket.recv(1024)  # Receive up to 1024 bytes at a time
        if not chunk:  # If no data is received (i.e., end of data), exit the loop
            break
        response += chunk  # Append the received chunk to the response variable

    # Decode the received byte data into a string and print it
    print(response.decode())

    # Close the socket connection after receiving the complete response
    clientSocket.close()
    print("Connection closed")

# Handle any exceptions that may occur during the connection or data transfer
except Exception as e:
    print(f"Error: {e}")  # Print the error message if an exception is raised