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


        //? We add all infos into the web page by creating divs
        for (var i = 0; i < length; i++) {
            console.log("Adding recipe " + i + "informations ...");
            var div = document.getElementById("recipes-container");
            div.innerHTML +=
                "<br>" +
                "<div class='recipe-title'>" + data[i]['title'] + "</div>" +
                "<div class='recipe-healthScore'>" + "HealthScore : " + data[i]["healthScore"] + "%" + "</div>" +
                "<div class='recipe-preparationTime'>" + "Preparation time : " + data[i]["preparationTime"] + "min for " + data[i]["nbrServings"] + " persons" + "</div>" +
                "<div class='recipe-image'><img src='" + data[i]["image"] + "'></div>"+
                "<br>";

        }    
        //TODO We add the event listener to the divs

          
    }
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