import socket


def client_program():
    host = "127.0.0.1"  # as both code is running on same pc
    port = 20001  # socket server port number

    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)  # instantiate
    UDPClientSocket.connect((host, port))  # connect to the server

    message = input(" -> ")  # take input

    while message.lower().strip() != 'bye':
        UDPClientSocket.send(message.encode())  # send message
        data = UDPClientSocket.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

        message = input(" -> ")  # again take input

    UDPClientSocket.close()  # close the connection


if __name__ == '__main__':
    client_program()