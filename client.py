import argparse
from socket import *

parser = argparse.ArgumentParser()

parser.add_argument('-i','--server_ip', type=str, required=True)
parser.add_argument('-p','--server_port', type=int, required=True)
parser.add_argument('-f','--filename',type=str,required=True)

args = parser.parse_args()

server_ip = args.server_ip
server_port = args.server_port
filename = args.filename

clientSocket = socket(AF_INET, SOCK_STREAM)

try:
    clientSocket.connect((server_ip,server_port))
    print(f"Connected to {server_ip} on port {server_port} using file {filename}")

    get_request = f"GET /{filename} HTTP/1.1\r\nHost: {server_ip}:{server_port}\r\nConnection: close\r\n\r\n"
    print("GET request: ", get_request)

    clientSocket.send(get_request.encode())

    response = b""

    while True:
        chunk = clientSocket.recv(1024)
        if not chunk:
            break
        response += chunk


    print(response.decode())

    clientSocket.close()
    print("Connection closed")




except Exception as e:
    print(f"Error:{e}")