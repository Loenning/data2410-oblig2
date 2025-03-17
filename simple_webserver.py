#import socket module
from socket import *
import sys # In order to terminate the program
serverSocket = socket(AF_INET, SOCK_STREAM) 

#Prepare a server socket
port = 8000
server_ip ='127.0.0.1'
serverSocket.bind((server_ip, port)) #Binds to localhost and port 8000
serverSocket.listen(1)


while True:
	#Establish the connection print('Ready to serve...') connectionSocket, addr = 
	try:
		print('Server is ready to receive connections...')

		connectionSocket, addr = serverSocket.accept()
		print(f"Connection from {addr}")

		
		message = connectionSocket.recv(1024).decode() 
		filename = message.split()[1]
		f = open(filename[1:])
		outputdata = f.read()

		#Send one HTTP header line into socket
		connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
		connectionSocket.send("Content-Type: text/html\r\n\r\n".encode())
		

		#Send the content of the requested file to the client 
		for i in range(0, len(outputdata)):
			connectionSocket.send(outputdata[i].encode()) 
		connectionSocket.send("\r\n".encode())
		connectionSocket.close()

	
	except IOError:
		#Send response message for file not found
		connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())
		connectionSocket.send("Content-Type: text/html\r\n\r\n".encode())
		connectionSocket.send("<html><body><h1>404 Not Found</h1></body></html>".encode())

		#Close client socket
		connectionSocket.close()
		
		
	break

serverSocket.close()
sys.exit()#Terminate the program after sending the corresponding data