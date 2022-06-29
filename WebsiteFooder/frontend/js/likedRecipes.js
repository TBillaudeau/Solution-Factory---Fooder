var xhr = null;


getXmlHttpRequestObject = function () {
    if (!xhr) {
        // Create a new XMLHttpRequest object 
        xhr = new XMLHttpRequest();
    }
    return xhr;
};


//? Function who start when the page run and add all recipes
function initListRecipes() {
    console.log("Starting init of the list of the recipes ...");
    getInfosRecipe();
}

function addInfosRecipe() {
    //? Check response is ready or not
    if (xhr.readyState == 4 && xhr.status == 201) {
        data = xhr.responseText;

        //? We convert the data who is a string into a dictionary
        var data = JSON.parse(data);

        console.log("Received data !");
        console.log(data);

        console.log("Length:");
        var length = Object.keys(data).length;
        console.log(length);

        //? Show a message if there is no recipe
        if (length == 0) {
            var div = document.getElementById("recipes-container");
            div.innerHTML +=
                "<div class='info-container'>You didn't like any recipes ... </div>";
        }


        //? We add all infos into the web page by creating divs
        for (var i = 0; i < length; i++) {
            console.log("Adding recipe " + i + " informations ...");
            var div = document.getElementById("recipes-container");
            div.innerHTML +=
                "<br>" +
                "<a onclick='showInfosRecipe("+ data[i]['id'] +")' class='recipe-title'>" + data[i]['title'] + "</a>" +
                "<div class='recipe-healthScore'>" + "HealthScore : " + data[i]["healthScore"] + "%" + "</div>" +
                "<div class='recipe-preparationTime'>" + "Preparation time : " + data[i]["preparationTime"] + "min for " + data[i]["nbrServings"] + " persons" + "</div>" +
                "<br>"+
                "<div class='recipe-image'><img src='" + data[i]["image"] + "'></div>"+
                "<br>"+
                "<div class='recipe-delete'>" +
                "<button class='btn-delete-recipe' onclick='deleteRecipe(" + data[i]["id"] + ")'>Delete</button>" +
                "</div>" +
                "<br>";
        }    
          
    }
}

//? Function to delete a recipe from the liked list
function deleteRecipe(id) {
    console.log("Deleting recipe with id " + id + " ...");
    xhr = getXmlHttpRequestObject();
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 201) {
            console.log(xhr.responseText);
            window.location.reload();
        }
    }
    xhr.open("POST", "http://localhost:6969/delete-recipe", true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({"id": id}));
}

//? Function to acces a web page who will show all informations of the recipe (from liked list of recipes)
function showInfosRecipe(id) {
    console.log("Id of recipe: "+id);
    //? We redirect the user to the web page who will show all informations of the recipe and add data of the recipe into the url
    window.location.href = "InfoRecipe.html?id=" + id + "&";
}


function getInfosRecipe() {
    xhr = getXmlHttpRequestObject();
    xhr.onreadystatechange = addInfosRecipe;
    // asynchronous requests
    xhr.open("POST", "http://localhost:6969/get-infos-recipe", true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    // Send the request over the network
    xhr.send();
}