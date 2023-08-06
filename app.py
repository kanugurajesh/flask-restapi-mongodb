from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)
api = Api(app)

# mongodb connection url
uri = "mongodb+srv://hasura:RsEB60OKT1ON0veq@cluster0.wg3z167.mongodb.net/?retryWrites=true&w=majority"

# database name and collection name
database_name = "rajesh"
collection_name = "rajesh"

# connect to mongodb
client = MongoClient(uri, server_api=ServerApi('1'))
db = client[database_name]
collection = db[collection_name]

# create a class for the resource
class UsersResource(Resource):
    def get(self):
        documents = list(collection.find())
        for document in documents:
            document["_id"] = str(document["_id"])

        return jsonify(documents)

    def post(self):
        data = request.json
        user_dict = {"id": data.get("id"),
                     "name": data.get("name"),
                     "email": data.get("email"),
                     "password": data.get("password")}
        result = collection.insert_one(user_dict)
        if result.inserted_id:
            return jsonify({"message": "User added successfully"})
        else:
            return jsonify({"error": "Invalid data"})

# create a class for the resource
class UserResource(Resource):
    def get(self, id):
        return jsonify(collection.find_one({"id": id}))

    def put(self, id):
        data = request.json
        user_dict = {"id": data.get("id"),
                     "name": data.get("name"),
                     "email": data.get("email"),
                     "password": data.get("password")}
        result = collection.update_one({"id": id}, {"$set": user_dict})
        if result.inserted_id:
            return jsonify({"message": "User data updated successfully"})
        else:
            return jsonify({"error": "Invalid data"})

    def delete(self, id):
        result = collection.delete_one({"id": id})
        if result.inserted_id:
            return jsonify({"message": "User deleted successfully"})
        else:
            return jsonify({"error": "Invalid data"})

# add the resource to the api
api.add_resource(UsersResource, '/users')
api.add_resource(UserResource, '/users/<int:id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=False)
