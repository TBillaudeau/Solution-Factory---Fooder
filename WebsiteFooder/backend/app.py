
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
import seaborn as sns
import matplotlib.pyplot as plt
from math import ceil
import re
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity,cosine_distances
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer

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

dietaryUser = {
    'vegetarian': False,
    'vegan': False,
    'sustainable': False,
    'cheap': False,
    'glutenFree': False,
    'dairyFree': False,
}
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
        elif like_or_dislike['data'] == 3:
            #? User chosen to skip this recipe
            with open('lastRecipeID.txt', 'r') as f:
                lastRecipeID = f.read()
            print("Recipe not added to any list")
        elif like_or_dislike['data'] == 2:
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

        print("User asked for list of recipes, list of recipes liked : " , list_recipes_id_liked)

        #? We now add the name, the healthscore, the preparation time and the image of each recipe to the dict
        i = 0

        for index, row in df.iterrows():
            if row['id'] in list_recipes_id_liked:
                recipes_infos[i] = {
                    'id' : row['id'],
                    'title': row['title'],
                    'healthScore': row['healthScore'],
                    'preparationTime': row['readyInMinutes'], 
                    'nbrServings': row['servings'],
                    'image': row['image'],
                    'price': row['pricePerServing']
                }
                print("Added recipe to dict" , recipes_infos)
                i += 1

        #? Convert the data to json   
        return_data = json.dumps(recipes_infos , cls = NpEncoder)

        #? Return the data
        return flask.Response(response = return_data, status=201)

@app.route("/delete-recipe", methods=["POST"])
def delete_recipe():
    if request.method == "POST":
        #? Get the id of the recipe to delete
        id_recipe = request.get_json()
        id_recipe = id_recipe['id']
        print("ID of the recipe to delete: ",id_recipe)

        #? Check if the recipe is in the list of liked recipes
        if id_recipe in list_recipes_id_liked:
            #? Remove the recipe from the list of liked recipes
            list_recipes_id_liked.remove(id_recipe)
            print("Removed recipe from liked list (", id_recipe ,"), list updated: " , list_recipes_id_liked)
        else:
            print("Error, recipe not found in the list of liked recipes")
        return flask.Response(response = "Recipe deleted", status=201)

@app.route("/get-infos-recipe-liked" , methods=["POST"])
def get_infos_recipe_liked():
    if request.method == "POST":
        #? We get the id
        id_recipe = request.get_json()["id"]
        id_recipe = int(id_recipe[0])

        #? We create a dict who will contain all the recipes infos so we can show them on the site
        recipes_infos = {}

        #? We now add all the infos

        for index, row in df.iterrows():
            if row['id'] == id_recipe:
                print("TITLE: ",row['title'])
                recipes_infos = {
                    #! ID
                    'id' : row['id'],
                    #! Title
                    'title': row['title'],
                    #! Summary
                    'summary': row['summary'],
                    #! Dish Type
                    'dishTypes': row['dishTypes'],
                    #! Image
                    'image': row['image'],
                    #! Liste ingrédients
                    'ingredients': row['extendedIngredients'],
                    #! Nbr servings
                    'nbrServings': row['servings'],
                    #! Allergenes
                    'vegan': row['vegan'],
                    'vegetarian': row['vegetarian'],
                    'glutenFree': row['glutenFree'],
                    'dairyFree': row['dairyFree'],
                    'sustainable': row['sustainable'],
                    #! Healthscore
                    'healthScore': row['healthScore'],
                    #! Cooking time
                    'cookingMinutes': row['cookingMinutes'],
                    #! Preparation time
                    'preparationTime': row['readyInMinutes'], 
                    #! Temps total
                    'totalTime': (row['cookingMinutes'] + row['readyInMinutes']),
                    #! Etapes recette
                    'instructions': row['instructions'],
                    #! Prix
                    'pricePerServing': row['pricePerServing'],
                }
                print("Added recipe to dict" , recipes_infos)

        #? Convert the data to json   
        return_data = json.dumps(recipes_infos , cls = NpEncoder)

        #? Return the data
        return flask.Response(response = return_data, status=201)


#* Store dietary restrictions
@app.route("/get-dietary-restrictions", methods=["GET" , "POST"])
def get_dietary_restrictions():
    if request.method == "POST":
        #? Retrieve the data
        dietary = request.get_json()

        #? Update the dietary stored of the user so we can filter the recipes
        dietaryUser['vegetarian'] = dietary['vegetarian']
        dietaryUser['vegan'] = dietary['vegan']
        dietaryUser['sustainable'] = dietary['sustainable']
        dietaryUser['cheap'] = dietary['cheap']
        dietaryUser['glutenFree'] = dietary['glutenFree']
        dietaryUser['dairyFree'] = dietary['dairyFree']

        #? Return confirmation
        return flask.Response(response = "Dietary updated", status=201)

#! Register a user
@app.route("/register-user", methods=["GET" , "POST"])
def register_user():
    if request.method == "POST":
        print("User asked to register: " , request.get_json())

        #? Retrieve the data
        userInfos = request.get_json()

        #? Open the json file and add it to a DF
        df = pd.read_json('user.json', orient='records')

        #? add a new row to the dataframe with entries from the user
        new_row = {
            "Name": userInfos['firstName'],
            "LastName": userInfos['lastName'],
            "BirthDay": userInfos['birthdate'], 
            "Email": userInfos['email'], 
            "Password": userInfos['password'],
            "LikedRecipes": [],
            "UnlikedRecipes": [],
            "Vegetarian": False,
            "Vegan": False,
            "EcoFriendly": False,
            "VeryHealthy": False,
            "GlutenFree": False,
            "DairyFree": False,
        }
        df = df.append(new_row, ignore_index=True)

        #? Save the dataframe into the json file
        df.to_json('user.json')

        #? Return confirmation
        return flask.Response(response = "success", status=200)

@app.route("/login-user", methods=["GET" , "POST"])
def login_user():
    if request.method == "POST":
        print("User asked to login: " , request.get_json())

        #? Retrieve the data
        userInfos = request.get_json()

        #? Open the json file and add it to a DF
        df = pd.read_json('user.json', orient='records')

        #? Check if the user exists
        if userInfos['email'] in df['Email'].values:
            #? Check if the password is correct
            if userInfos['password'] == df.loc[df['Email'] == userInfos['email']]['Password'].values[0]:
                #? Return the user infos
                print("User successfully logged in")

                return flask.Response(response = "success", status=200)
            else:
                #? Return error
                return flask.Response(response = "error", status=401)
        else:
            #? Return error
            return flask.Response(response = "error", status=401)


#! ###########################
#! Recommendation system
#! ###########################

# Chargement des données & Nettoyage des données
data = pd.read_json('recipes.json')
data = data.dropna(axis=1)
data = data.drop(columns=['cheap','cookingMinutes','preparationMinutes','sustainable','openLicense','analyzedInstructions','instructions'])

# Nettoyage Colonne Summary
netoyage_html = lambda x: re.sub("<.*?>", " ", x).lower()
netoyage_ponctuation = lambda x: re.sub(r'[^\w\s]',' ',x)

data['summary'] = data['summary'].apply(netoyage_html)
data['summary'] = data['summary'].apply(netoyage_ponctuation)

#Normalisation des données
vectorizer = CountVectorizer()
nltk.download('stopwords')
nltk.download('wordnet')

stop_words = set(stopwords.words('english')) 

tokenized=word_tokenize(data["summary"][0])
stop_words = stopwords.words('english')

filtered = [word for word in tokenized if word not in stop_words]

stemmer = PorterStemmer()
filtered = [stemmer.stem(J) for J in filtered]
' '.join(filtered)

stop_words = stopwords.words('english')
stemmer = PorterStemmer()
preprocess = lambda x: ' '.join([stemmer.stem(word) for word in word_tokenize(x) if word not in stop_words])
rm_digits = lambda x: ''.join([i for i in x if not i.isdigit()])

data['parsed']=data['summary'].apply(preprocess)
data['parsed']=data['summary'].apply(rm_digits)
                       

vectorizer = CountVectorizer()
matrix=vectorizer.fit_transform(data['parsed'])

vectorizer.get_feature_names()
counts = pd.DataFrame(matrix.toarray(),columns=vectorizer.get_feature_names_out())

data=data.drop(columns=['veryHealthy','veryPopular','gaps'])

#One hot encoding
joined_lists=lambda x: ','.join(x)

cuis=data["cuisines"].apply(joined_lists).str.get_dummies(",")
df_reco=pd.concat([data,cuis],axis=1)
df_reco=df_reco.drop(columns=["cuisines"])

dish=data["dishTypes"].apply(joined_lists).str.get_dummies(",")
df_reco=pd.concat([df_reco,dish],axis=1)
df_reco=df_reco.drop(columns=["dishTypes"])

diets=data["diets"].apply(joined_lists).str.get_dummies(",")
df_reco=pd.concat([df_reco,diets],axis=1)
df_reco=df_reco.drop(columns=["diets"])

occ=data["occasions"].apply(joined_lists).str.get_dummies(",")
df_reco=pd.concat([df_reco,occ],axis=1)
df_reco=df_reco.drop(columns=["occasions"])

df_reco['vegetarian'] = df_reco['vegetarian'].astype(int)
df_reco['vegan'] = df_reco['vegan'].astype(int)
df_reco['glutenFree'] = df_reco['glutenFree'].astype(int)
df_reco['dairyFree'] = df_reco['dairyFree'].astype(int)
df_reco['weightWatcherSmartPoints'] = df_reco['weightWatcherSmartPoints'].astype(int)

df_reco = df_reco[['vegetarian', 'vegan', 'glutenFree', 'dairyFree',
       'weightWatcherSmartPoints', 'healthScore',
       'pricePerServing', 'readyInMinutes',
       'servings',
       'American', 'Asian', 'Chinese', 'European', 'French', 'Indian',
       'Italian', 'Jewish', 'Korean', 'Mediterranean', 'Southern',
       'Vietnamese', 'antipasti', 'antipasto', 'appetizer', 'beverage',
       'bread', 'breakfast', 'brunch', 'condiment', 'dessert', 'dinner', 'dip',
       'drink', 'fingerfood', 'hor d\'oeuvre', 'lunch', 'main course',
       'main dish', 'morning meal', 'salad', 'sauce', 'side dish', 'snack',
       'soup', 'spread', 'starter', 'dairy free', 'fodmap friendly',
       'gluten free', 'ketogenic', 'lacto ovo vegetarian', 'paleolithic',
       'pescatarian', 'primal', 'vegan', 'whole 30', '4th of july',
       'christmas', 'easter', 'fall', 'father\'s day', 'halloween', 'hanukkah',
       'summer', 'super bowl', 'thanksgiving', 'valentine\'s day', 'winter']]


#enlève les colonnes indentiques
df_reco= df_reco.T.drop_duplicates().T

counts=counts.drop(columns=['al','all','and','very','up','are','as','at','de','in','is','it','la','no','we','not','you','your','add','about','again'])

df_reco=pd.concat([df_reco,counts],axis=1)


def recommandation_par_preference(df_reco,pref : list, dislike: list,nb_recommandations=1):
    similarity=cosine_similarity(df_reco)
    distance=cosine_distances(df_reco)
    
    tab=np.array([0  for i in range(100)])
    for i in pref:
        index = data.index[data['id'] == i].tolist()[0]
        tab = np.add(tab,np.array(similarity[index-1]))
        
    for j in dislike:
        index = data.index[data['id'] == j].tolist()[0]
        tab = np.add(tab,np.array(distance[index-1]))
    
    pref = [data.index[data['id'] == i].tolist()[0]-1 for i in pref]
    dislike = [data.index[data['id'] == i].tolist()[0]-1 for i in dislike]
    tab = np.delete(tab, pref)
    tab = np.delete(tab, dislike)

    indices_ascending=(np.argsort(tab))
    indices_descending=indices_ascending[::-1]
    return data.iloc[indices_descending[0]].id


@app.route("/get-recipe-reco", methods=["GET" , "POST"])
def get_recipe_reco():
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
        elif like_or_dislike['data'] == 3:
            #? User chosen to skip this recipe
            with open('lastRecipeID.txt', 'r') as f:
                lastRecipeID = f.read()
            print("Recipe not added to any list")
        elif like_or_dislike['data'] == 2:
            pass
            #? it's the first recipe shown to the user so we don't need to do anything here

        #! ---------------------
        #! Get the recipe 
        #! ---------------------
        id_recipe_reco = recommandation_par_preference(df_reco,list_recipes_id_liked, list_reciped_id_disliked,nb_recommandations=1)
        print("Received recipe id from reco system: ", id_recipe_reco)

        #recipe_reco = df.loc[id_recipe_reco]
        recipe_reco = df[df['id']==id_recipe_reco]
        print("Received recipe from reco system: ", recipe_reco)

        print(recipe_reco['title'].values)
        this_title = recipe_reco['title'].values[0]
        print("Title: ",this_title)
        this_image = recipe_reco['image'].values[0]
        print("Image: ",this_image)
        this_healthscore = recipe_reco['healthScore'].values[0]
        print("Healthscore: ",this_healthscore)

        #? We add the ID of the recipe to a txt file
        lastRecipeID = recipe_reco['id'].values[0]
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



#? Run Flask App
if __name__ == "__main__":
    app.run("localhost", 6969)
