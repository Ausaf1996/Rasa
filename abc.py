import pymongo
import json
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["rasa"]
mycol = mydb["Time"]
x = mycol.distinct("sender_id")
mydict = {"sender_id": "20-01-2020", "9-10am": "", "10-11am": "", "2-3pm": "", "3-4pm": ""}
y = mycol.insert_one(mydict)