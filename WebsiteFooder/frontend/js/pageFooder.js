var xhr = null;

getXmlHttpRequestObject = function () {
    if (!xhr) {
        // Create a new XMLHttpRequest object 
        xhr = new XMLHttpRequest();
    }
    return xhr;
};
 
function initFirstRecipe() {
    console.log("Web page loaded !");
    getInfos(2);
    console.log("Starting init of the first recipe ...");
}

function addInfos() {
    // Check response is ready or not
    if (xhr.readyState == 4 && xhr.status == 201) {
        // Check response is ready or not
        data = xhr.responseText;

        // We convert the data who is a string into a dictionary
        var dictionary = JSON.parse(data);

        console.log("Received data on the next recipe !");
        console.log(dictionary);

        // We add all infos into the web page
        titleDiv = document.getElementById('title-container');
        imgDiv = document.getElementById('image-container');
        healthDiv = document.getElementById('healthScore-container');

        //! Check for empty data
        // if (dictionary.title == " ") {
        //     console.log("NO DATA FOR TITLE, skipping ...")
        //     getInfos(3)
        // }

        titleDiv.innerHTML = dictionary['title'];
        imgDiv.src = dictionary['image'];
        healthDiv.innerHTML = dictionary['healthScore'];
    }
}

function likeORdislike(value) {
    if (value == 1) {
        console.log("User liked the recipe !");
    }
    else if (value == 0) {
        console.log("User disliked the recipe :/");
    }
    else {
        console.log("User skiped the recipe...");
    }
}

function getInfos(like_or_dislike) {
    likeORdislike(like_or_dislike);
    xhr = getXmlHttpRequestObject();
    xhr.onreadystatechange = addInfos;
    // asynchronous requests
    xhr.open("POST", "http://localhost:6969/get-recipe", true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    // Send the request over the network
    xhr.send(JSON.stringify({"data": like_or_dislike}));
}

function getInfosReco(like_or_dislike) {
    likeORdislike(like_or_dislike);
    xhr = getXmlHttpRequestObject();
    xhr.onreadystatechange = addInfos;
    // asynchronous requests
    xhr.open("POST", "http://localhost:6969/get-recipe-reco", true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    // Send the request over the network
    xhr.send(JSON.stringify({"data": like_or_dislike}));
}
