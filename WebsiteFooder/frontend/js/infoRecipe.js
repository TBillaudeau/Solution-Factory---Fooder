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
            var div = document.getElementById("recipe-infos");
            div.innerHTML +=
                "<div class='recipe-title'>" + data["title"] + "</div>" +
                "<div class='recipe-summary'>" + data["summary"] + "</div>" +
                "<div class='recipe-ingredients'>" + data["ingredients"][0]["name"] + "</div>" +
                "<div class='recipe-ingredients'>" + data["ingredients"][0]["amount"] + "</div>" +
                "<div class='recipe-totalTime'>" + data["totalTime"] + " minutes</div>" +
                "<br>";
        }    
    }
    xhr.open("POST", "http://localhost:6969/get-infos-recipe-liked", true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({"id": id}));
}
