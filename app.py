from flask import Flask, request, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

class UserAPI:
    def __init__(self, uri, database_name="rajesh", collection_name="rajesh"):
        self.app = Flask(__name__)
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]

        @self.app.route('/')
        def message():
            return "<html><body><h1>Hi, welcome to the RestApi built using Flask. You are currently at the root URL</h1></body></html>"

        @self.app.route('/users')
        def users():
            return str(list(self.collection.find()))

        @self.app.route('/users/<int:user_id>')
        def get_user(user_id):
            return str(self.collection.find_one({"id": user_id}))

        @self.app.route('/users', methods=['POST'])
        def create_user():
            data = request.json
            if data:
                user_dict = {"id": data.get("id"),
                             "name": data.get("name"),
                             "email": data.get("email"),
                             "password": data.get("password")}
                result = self.collection.insert_one(user_dict)
                if result.inserted_id:
                    return jsonify({"message": "User inserted successfully"}), 201
                else:
                    return jsonify({"error": "Invalid data"}), 400

        @self.app.route('/users/<int:id>', methods=["POST"])
        def update_user(id):
            data = request.json
            if data:
                user_dict = {"id": data.get("id"),
                             "name": data.get("name"),
                             "email": data.get("email"),
                             "password": data.get("password")}
                result = self.collection.update_one({"id": id}, {"$set": user_dict})
                if result.modified_count:
                    return jsonify({"message": "User updated successfully"}), 200
                else:
                    return jsonify({"error": "Invalid data"}), 400

        @self.app.route('/users/<int:id>', methods=["DELETE"])
        def delete_user(id):
            result = self.collection.delete_one({"id": id})
            if result.deleted_count:
                return jsonify({"message": "User deleted successfully"}), 200
            else:
                return jsonify({"error": "User not found"}), 404
            
if __name__ == '__main__':
    uri = "mongodb+srv://hasura:RsEB60OKT1ON0veq@cluster0.wg3z167.mongodb.net/?retryWrites=true&w=majority"
    user_api = UserAPI(uri)
    user_api.app.run(host='0.0.0.0', port=5000,debug=False)