var xhr = null;

getXmlHttpRequestObject = function () {
    if (!xhr) {
        // Create a new XMLHttpRequest object 
        xhr = new XMLHttpRequest();
    }
    return xhr;
};

function addDietary() {

}

//TODO Finish this
function updateDietary() {
    xhr = getXmlHttpRequestObject();
    xhr.onreadystatechange = addDietary;
    // asynchronous requests
    xhr.open("POST", "http://localhost:6969/get-dietary-restrictions", true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    // Send the request over the network
    xhr.send();
}
