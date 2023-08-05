# Importing the flask module in the project is mandatory.
from flask import *  

# Flask constructor takes the name of current module (__name__) as argument.
app = Flask(__name__)

# Import MongoClient from pymongo so we can connect to the database
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Create a URI to connect to MongoDB Atlas
uri = "mongodb+srv://hasura:RsEB60OKT1ON0veq@cluster0.wg3z167.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
    db = client['rajesh']
    collection = db['rajesh']

# If an exception is raised, then the server is not available
except Exception as e:
    print(e)

# A decorator used to tell the application
@app.route('/')  
def message():  
      return "<html><body><h1>Hi, welcome to the RestApi build using flask you are currently at the root url</h1></body></html>"

# returning all the users from the mongodb database
@app.route('/users')
def users():
    # return all the documents in the 'users' collection
    return str(list(collection.find()))

# returning the user with the given user_id from the mongodb database
@app.route('/users/<int:user_id>')
def get_user(user_id):
    # return the user with the given user_id
    return str(collection.find_one({"id": user_id}))

# creating a new user in the mongodb database
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json  # Assuming you are sending JSON data in the request
    if data:
        user_dict = {"id": data.get("id"),
                     "name": data.get("name"),
                     "email": data.get("email"),
                     "password": data.get("password")}
        result = collection.insert_one(user_dict)
    if result.inserted_id:
        return jsonify({"message": "User inserted successfully"}), 201
    else:
        return jsonify({"error": "Invalid data"}), 400  # Bad Request

# updating the user with the given user_id in the mongodb database
@app.route('/users/<int:id>',methods=["POST"])
def update_user(id):
    data = request.json  # Assuming you are sending JSON data in the request
    if data:
        user_dict = {"id": data.get("id"),
                     "name": data.get("name"),
                     "email": data.get("email"),
                     "password": data.get("password")}
        
        result = collection.update_one({"id": id}, {"$set": user_dict})

    if result.modified_count:
        return jsonify({"message": "User updated successfully"}), 200
    else:
        return jsonify({"error": "Invalid data"}), 400

# deleting the user with the given user_id in the mongodb database
@app.route('/users/<int:id>',methods=["DELETE"])
def delete_user(id):
    # delete the user with the given user_id
    result = collection.delete_one({"id": id})
    if result.deleted_count:
        return jsonify({"message": "User deleted successfully"}), 200
    else:
        return jsonify({"error": "User not found"}), 404

# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application on the local development server. Debug is set to false in production mode but keep it to true in development mode
   app.run(debug = False)#    