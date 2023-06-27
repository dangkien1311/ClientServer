import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Demo"]
mycol = mydb["Colection"]

# myquery = {"msg" : "send"}

mydoc = mycol.find()
# queryResult = str()
# for x in mydoc:
#   queryResult += x + ":" + mydoc[x]
queryResult = str(mydoc)

print(queryResult)