from pymongo import MongoClient
from bson.objectid import ObjectId

mongodb_client = None
database = None

def get_db():
    global mongodb_client, database
    if not mongodb_client:
        mongodb_client = MongoClient("mongodb+srv://ttnhan:1@cluster0.xpzciub.mongodb.net/")
        database = mongodb_client["research-agent"]
    return database

def find_by_id(collections, id):
    return collections.find_one({"_id": ObjectId(id)})