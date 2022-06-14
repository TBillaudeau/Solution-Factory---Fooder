from flask import Flask, request
import flask
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    return "Hello, World!"

#! ############################
#! Recipes
#! ############################

img = "https://spoonacular.com/recipeImages/664288-556x370.jpg"

@app.route("/image", methods=["GET"])
def get_image():
    if request.method == "GET":
        return flask.jsonify(img)



#! ############################
#! Flask App TESTS TESTS
#! ############################

@app.route('/users', methods=["GET", "POST"])
def users():
    print("users endpoint reached...")
    if request.method == "GET":
        with open("users.json", "r") as f:
            data = json.load(f)
            data.append({
                "username": "user4",
                "pets": ["hamster"]
            })

            return flask.jsonify(data)
    if request.method == "POST":
        received_data = request.get_json()
        print(f"received data: {received_data}")
        message = received_data['data']
        return_data = {
            "status": "success",
            "message": f"received: {message}"
        }
        return flask.Response(response=json.dumps(return_data), status=201)


#? Run Flask App
if __name__ == "__main__":
    app.run("localhost", 6969)