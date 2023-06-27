import socket
import pymongo as Mongo
from pymongo import MongoClient
from json import dumps
import json

class UserInfo:
  def __init__(self, userid, name):
    self.userid = userid
    self.name = name

def server_program():
    localIP     = "127.0.0.1"

    localPort   = 20001

    bufferSize  = 1024

    msgFromServer = "Recieved"

    bytesToSend = str.encode(msgFromServer)

    #connect to database

    Mongo_client = MongoClient('mongodb://localhost:27017/')

    database = "Demo"

    collection ="Colection"
    
    db = Mongo_client.get_database(database)

    col = db.get_collection(collection)


    # Create a datagram socket

    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # Bind to address and ip

    UDPServerSocket.bind((localIP, localPort))
    print("UDP server up and listening")

    # Listen for incoming datagrams

    while(True):

        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

        message = bytesAddressPair[0].decode()

        address = bytesAddressPair[1]

        clientMsg = "Message from Client:{}".format(message)
        clientIP  = "Client IP Address:{}".format(address)

        print(clientMsg)
        print(clientIP)
        # Create user
        if str(message) == "register":
            try:
                print("Create collection")
                new_collection = str(address)
                col = db.create_collection(new_collection)
            except:
                 msgFromServer = "User already exist"
                 bytesToSend = str.encode(msgFromServer)

        # catch event
        elif str(message) == "send":
            col.insert_one(
                {
                    "name": "send event", 
                    "msg" : message
                 }
            )
            print("send to database")

        # Sending json file to mongodb
        elif str(message) == "json":
            with open('data.json') as file:
                file_json_data = json.load(file)
            col.insert_many(file_json_data)

        # Sending object to mongodb
        elif str(message) == "object":
            user1  = UserInfo(23243, "kien")
            jsonstr = json.dumps(user1.__dict__)
            result = json.loads(jsonstr)
            col.insert_one(result)
         

        # Sending a reply to client
        UDPServerSocket.sendto(bytesToSend, address)
    # UDPServerSocket.close()
if __name__ == '__main__':
    server_program()