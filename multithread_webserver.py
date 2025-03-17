from socket import *
import _thread as thread
import sys
import time

def now():
    return time.ctime(time.time())

def handleClient(connectionSocket):
    try:

        time.sleep(3)

        message = connectionSocket.recv(1024).decode()

        if not message:
            connectionSocket.close()
            return
        
        filename = message.split()[1]

        try:
            f = open(filename[1:])
            outputdata = f.read()

            connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
            connectionSocket.send("Content-Type: text/html\r\n\r\n".encode())

            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i].encode())
            connectionSocket.send("\r\n".encode())
        
        except FileNotFoundError:
            connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())
            connectionSocket.send("Content-Type: text/html\r\n\r\n".encode())
            connectionSocket.send("<html><body><h1>404 Not Found</h1></body></html>".encode())
        
    except Exception as e:
        print(f"Error handling client: {e}")
    
    finally:
        connectionSocket.close()


def main():

    serverSocket = socket(AF_INET, SOCK_STREAM)

    port = 8000
    server_ip ='127.0.0.1'

    try:
        serverSocket.bind((server_ip,port))
    except:
        print("Failed to bind. Error : ")
        sys.exit()

    serverSocket.listen(5)
    print('Server is ready to receive connections...')

    connection_count = 0

    while True:
        
        connectionSocket, addr = serverSocket.accept()
        print(f"Connection from {addr}")
        print(f"at ", now())

        thread.start_new_thread(handleClient, (connectionSocket,))

        connection_count += 1

    #serverSocket.close()
    #sys.exit()#Terminate the program after sending the corresponding data


if __name__=='__main__':
    main()
