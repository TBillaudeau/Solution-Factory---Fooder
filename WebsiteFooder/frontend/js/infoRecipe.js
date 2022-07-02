var xhr = null;

getXmlHttpRequestObject = function () {
    if (!xhr) {
        // Create a new XMLHttpRequest object 
        xhr = new XMLHttpRequest();
    }
    return xhr;
};



//! Function to retrieve data from an URL
function getUrlParamArray(param) {
    param = param.replace(/([\[\](){}*?+^$.\\|])/g, "\\$1");
    var value = [];
    var regex = new RegExp("[?&]" + param + "=([^&#]*)", "g");
    var url   = decodeURIComponent(window.location.href);
    var match = null;
    while (match = regex.exec(url)) {
        value.push(match[1]);
    }    
    return value;
}

//? Function to show all the informations of a recipe
function initRecipeInfos(){
    //? Get the id of the recipe
    var id = getUrlParamArray("id");
    console.log("Id of recipe: "+id);

    //? We retrieve all the data we need for this recipe
    xhr = getXmlHttpRequestObject();
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 201) {
            var data = JSON.parse(xhr.responseText);
            console.log("Received data !");
            console.log(data);

            //? We add all infos into the web page by creating divs
            
            console.log("Adding image ...")
            var divImage = document.getElementById("image-container");
            divImage.innerHTML += "<img alt='logo' src='" + data["image"] + "'>";

            
            console.log("Adding title ...")
            var divTitle = document.getElementById("title-container");
            divTitle.innerHTML += data["title"];
            var divTitle2 = document.getElementById("title-container2");
            divTitle2.innerHTML += data["title"];

            console.log("Adding ingredients ...")
            var divIngredients = document.getElementById("ingredients-container");
            for (i = 0 ; i < data["ingredients"].length ; i++) {
                divIngredients.innerHTML += data['ingredients'][i]['original'] + "<br>";
            }

            console.log("Adding dietary infos ...")
            var divDietary = document.getElementById("dietary-container");
            if (data["vegan"] == "True") {
                console.log("Vegan :" + data["vegan"]);
                divDietary.innerHTML += "Vegan <i class='fa-solid fa-badge-check'></i><br>";
            }
            else {
                console.log("Not vegan :" + data["vegan"]);
                divDietary.innerHTML += "Vegan <i class='fa-solid fa-circle-xmark'></i><br>";
            }

            if (data["vegetarian"] == "True") {
                console.log("Vegetarian");
                divDietary.innerHTML += "Vegetarian <i class='fa-solid fa-badge-check'></i><br>";
            }
            else {
                console.log("Not vegetarian");
                divDietary.innerHTML += "Vegetarian <i class='fa-solid fa-circle-xmark'></i><br>";
            }

            if (data["glutenFree"] == "True") {
                console.log("Gluten free");
                divDietary.innerHTML += "Gluten free <i class='fa-solid fa-badge-check'></i><br>";
            }
            else {
                console.log("Not gluten free");
                divDietary.innerHTML += "Gluten free <i class='fa-solid fa-circle-xmark'></i><br>";
            }

            if (data["dairyFree"] == "True") {
                console.log("Dairy free");
                divDietary.innerHTML += "Dairy free <i class='fa-solid fa-badge-check'></i><br>";
            }
            else {
                console.log("Not dairy free");
                divDietary.innerHTML += "Dairy free <i class='fa-solid fa-circle-xmark'></i><br>";
            }

            if (data["sustainable"] == true) {
                console.log("Sustainable");
                divDietary.innerHTML += "<div id='sustainable'>Sustainable</div><i class='fa-solid fa-badge-check'>";
            }

            var divHealthscore = document.getElementById("healthscore-container");
            if (data['healthScore'] != null) {
                console.log("Health score : " + data['healthScore']);
                divHealthscore.innerHTML += "Health score : " + data['healthScore'] + "%";
            }

            var divtotalTime = document.getElementById("totalTime-container");
            if (data['totalTime'] != null) {
                console.log("Total time : " + (data['totalTime']));
                divtotalTime.innerHTML += "Total time : " + (data['totalTime']) + " min";
            }

            var preparationTime = document.getElementById("preparationTime-container");
            if (data['preparationTime'] != null) {
                console.log("Preparation time : " + data['preparationTime']);
                preparationTime.innerHTML += "Preparation time : " + data['preparationTime'] + "min";
            }
            else {
                console.log("Preparation time : " + data['preparationTime']);
                preparationTime.innerHTML += "Preparation time : No data";
            }

            var cookingTime = document.getElementById("cookingTime-container");
            if (data['cookingMinutes'] != -1) {
                console.log("Cooking time : " + data['cookingMinutes']);
                cookingTime.innerHTML += "Cooking time : " + data['cookingMinutes'] + "min";
            }
            else {
                console.log("Cooking time : " + data['cookingMinutes']);
                cookingTime.innerHTML += "Cooking time : No time";
            }

            var divrecipeSteps = document.getElementById("recipesStep-container");
            instructionsRecipe = data['instructions'];
            // split the string into an array of instructions at each "."
            var instructions = instructionsRecipe.split(".");
            console.log(instructionsRecipe);
            for (i = 0; i < instructions.length-1; i++) {
                divrecipeSteps.innerHTML += "<h1>Step "+(i+1)+"</h1><br>" + instructions[i] + "\n<br><br>";
            }

        }    
    }
    xhr.open("POST", "http://localhost:6969/get-infos-recipe-liked", true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({"id": id}));
}
