import socket
import pymongo as Mongo
from pymongo import MongoClient

def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 3000  # initiate port no above 1024

    # Create socket object
    #Defaut socket type : TCP --> socket.SOCK_STREAM
    # UDP : socket.SOCK_DGRAM --> bilnd recive
    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together
    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        elif str(data) == "send":
            Mongo_client = MongoClient('mongodb://localhost:27017/')
            print("ok")
            db = Mongo_client.get_database("Demo")
            col = db.get_collection("Colection")
            col.insert_one(
                {"name":1234, "msg" : data}
            )
    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()