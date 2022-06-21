var xhr = null;

getXmlHttpRequestObject = function () {
    if (!xhr) {
        // Create a new XMLHttpRequest object 
        xhr = new XMLHttpRequest();
    }
    return xhr;
};

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

        titleDiv.innerHTML = dictionary['title'];
        imgDiv.src = dictionary['image'];
        healthDiv.innerHTML = dictionary['healthScore'];
    }
    if (xhr.status == 500) {
        getInfos();
    }
}

function getInfos() {
    xhr = getXmlHttpRequestObject();
    xhr.onreadystatechange = addInfos;
    // asynchronous requests
    xhr.open("POST", "http://localhost:6969/get-recipe", true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    // Send the request over the network
    xhr.send();
}
