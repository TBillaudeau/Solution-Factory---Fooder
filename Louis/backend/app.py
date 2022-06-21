
#! #################################
#! IMPORTS
#! #################################

from flask import Flask, request
import flask
import json
from flask.json import jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np

#! #################################
#! Setup Flask
#! #################################

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    return "Hello, World!"

#! #################################
#! Get recipes from API and json file 
#! #################################

#? Add data to a dataframe
df = pd.read_json('recipes.json', orient='records')

#? Keep only recipes with healthscore > (the value could be higher for healthier recipes but we are currently limited to the API)
df = df.loc[df['healthScore'] >= 50]

#! #################################
#! Link from recipes to the webiste 
#! #################################

#? For now, stores all recipes already proposed to the user
list_recipes_id_used = []

#! Function to return a random recipe not already proposed to the user
def get_random_recipe():
    #? Get a random recipe from the dataframe
    random_recipe = df.sample(1)

    #? Get the id of the recipe
    id_recipe = random_recipe['id'].values[0]

    #? Check if the recipe has already been proposed to the user
    if id_recipe in list_recipes_id_used:
        get_random_recipe()
    else:
        list_recipes_id_used.append(id_recipe)
        return random_recipe




@app.route("/get-recipe", methods=["GET" , "POST"])
def get_recipe():
    if request.method == "GET":
        return flask.jsonify("Please use POST method")
    elif request.method == "POST":
        #! ---------------------
        #! Get the recipe 
        #! ---------------------
        recipe = get_random_recipe()

        this_title = recipe['title'].values[0]
        print("Title: ",this_title)
        this_image = recipe['image'].values[0]
        print("Image: ",this_image)
        this_healthscore = recipe['healthScore'].values[0]
        print("Healthscore: ",this_healthscore)

        #? create dict data
        return_data = {
            'title': this_title,
            'image': this_image,
            'healthScore': this_healthscore
        }

        #? We need to create an encoder in order to convert the data to json
        class NpEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, np.integer):
                    return int(obj)
                if isinstance(obj, np.floating):
                    return float(obj)
                if isinstance(obj, np.ndarray):
                    return obj.tolist()
                return super(NpEncoder, self).default(obj)

        #? Convert the data to json   
        return_data = json.dumps(return_data , cls = NpEncoder)

        #? Return the data
        return flask.Response(response = return_data, status=201)






#! ############################
#! Flask App TESTS TESTS
#! ############################

# @app.route('/users', methods=["GET" , "POST"])
# def users():
#     print("users endpoint reached...")
#     if request.method == "GET":
#         with open("users.json", "r") as f:
#             data = json.load(f)
#             #? To add a new user to the users.json file
#             # data.append({
#             #     "username": "user4",
#             #     "pets": ["hamster"]
#             # })

#             return flask.jsonify(data)
    
#     if request.method == "POST":
#         received_data = request.get_json()
#         print(f"received data: {received_data}")
#         message = received_data['data']
#         title = "pizza"
#         img = 'https://spoonacular.com/recipeImages/664288-556x370.jpg'
#         return_data = {
#             "title": title,
#             "img": img
#         }
#         return flask.Response(response=json.dumps(return_data), status=201)


#? Run Flask App
if __name__ == "__main__":
    app.run("localhost", 6969)