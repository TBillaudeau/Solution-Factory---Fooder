
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

#TODO --------------------------------------------
#TODO Local variables until we work with a databse
list_recipes_id_used = []
list_recipes_id_liked = []
list_reciped_id_disliked = []
#TODO --------------------------------------------

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
        global lastRecipeID
        #! ---------------------
        #! Like or Dislike ?
        #! ---------------------
        #? First we check if the user liked or disliked the last recipe
        like_or_dislike = request.get_json()
        print("DATA like: ",like_or_dislike)

        if like_or_dislike['data'] == 1:
            with open('lastRecipeID.txt', 'r') as f:
                lastRecipeID = f.read()
            list_recipes_id_liked.append(int(lastRecipeID))
            print("Added recipe to liked list (", lastRecipeID ,"), list updated: " , list_recipes_id_liked)
        elif like_or_dislike['data'] == 0:
            with open('lastRecipeID.txt', 'r') as f:
                lastRecipeID = f.read()
            list_reciped_id_disliked.append(int(lastRecipeID))
            print("Added recipe to disliked list (", lastRecipeID ,"), list updated: " , list_reciped_id_disliked)
        else:
            pass
            #? it's the first recipe shown to the user so we don't need to do anything here

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

        #? We add the ID of the recipe to a txt file
        lastRecipeID = recipe['id'].values[0]
        with open('lastRecipeID.txt', 'w') as f:
            f.write(str(lastRecipeID))
            print("Added RECIPEID to txt file")

        #? create dict data
        return_data = {
            'title': this_title,
            'image': this_image,
            'healthScore': this_healthscore
        }

        #? Convert the data to json   
        return_data = json.dumps(return_data , cls = NpEncoder)

        #? Return the data
        return flask.Response(response = return_data, status=201)

@app.route("/get-infos-recipe", methods=["GET" , "POST"])
def get_infos_recipe():
    if request.method == "GET":
        return flask.jsonify("Please use POST method")
    elif request.method == "POST":
        #? We create a dict who will contain all the recipes infos so we can show them on the site
        recipes_infos = {}

        #! FO TEST PRUPOSES
        #list_recipes_id_liked = [652417 , 659135 , 665294 , 715447]

        print("User asked for list of recipes, list of recipes liked : " , list_recipes_id_liked)

        #? We now add the name, the healthscore, the preparation time and the image of each recipe to the dict
        i = 0

        #TODO PB ICI
        for index, row in df.iterrows():
            print("Index: ",index , "ID: ",row['id'])
            print(list_recipes_id_liked)
            if row['id'] in list_recipes_id_liked:
                recipes_infos[i] = {
                    'id' : row['id'],
                    'title': row['title'],
                    'healthScore': row['healthScore'],
                    'preparationTime': row['readyInMinutes'], 
                    'nbrServings': row['servings'],
                    'image': row['image']
                }
                print("Added recipe to dict" , recipes_infos)
                i += 1

        #? Convert the data to json   
        return_data = json.dumps(recipes_infos , cls = NpEncoder)

        #? Return the data
        return flask.Response(response = return_data, status=201)


#? Run Flask App
if __name__ == "__main__":
    app.run("localhost", 6969)