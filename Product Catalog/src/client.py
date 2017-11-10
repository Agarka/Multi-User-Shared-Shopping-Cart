from pymongo import MongoClient 
from bson.json_util import dumps
from bson.objectid import ObjectId
from pymongo import errors
from flask import jsonify
import json

'''Mongo Client object to do crud operations on MongoDB'''

class mongo_client:
    def __init__(self):
        try:
            self.client = MongoClient()
            self.db = self.client.books
            self.collection = self.db.books_collection
        except pymongo.errors.ConnectionFailure as e:
            return jsonify({"Status": "Error",\
                            "Message":"Connection lost with database server"})
        except pymongo.errors.ServerSelectionTimeoutError as e:
            return jsonify({"Status": "Error",\
                            "Message":"Could not connect to database server"})

   
    def get_all(self):
        try:
            output = self.collection.find()
            data = dumps(output)
        except Exception as e:
            return jsonify({"Status":"Error"})
        return jsonify({"Status": "OK", "data": json.loads(data)})

    def get_one(self,oid):
        try:
            output = self.find_one({'_id': ObjectId(oid)})
            data = dumps(output)
        except Exception as e:
            return jsonify({"Status":"Error"})
        return jsonify({"Status": "OK", "data": json.loads(data)})

    def put_one(self,oid):
        try:
            output = books.update_one({'_id': ObjectId(oid)},\
                                      {'$inc':{\
                                               'Qty': -1\
                                              }})
            data = dumps(output)
        except Exception as e:
            return jsonify({"Status":"Error"})
        return jsonify({"Status":"OK"})





if __name__ == "__main__":
    client = mongo_client()
    print(client.get_all())