var xhr = null;

getXmlHttpRequestObject = function () {
    if (!xhr) {
        // Create a new XMLHttpRequest object 
        xhr = new XMLHttpRequest();
    }
    return xhr;
};

//TODO A FINNIR
function registerUser(dataUser) {
    console.log("Registering user ...");
    console.log(dataUser);
}