var xhr = null;

getXmlHttpRequestObject = function () {
    if (!xhr) {
        // Create a new XMLHttpRequest object 
        xhr = new XMLHttpRequest();
    }
    return xhr;
};

function loginUser() {
    if (xhr.readyState == 4 && xhr.status == 200) {
        var response = xhr.responseText;
        if (response == "success") {
            alert("User successfully logged in");
            window.location.href = "../index.html";
        } else {
            alert("User does not exist");
            window.location.href = "../pageLogin.html";
        }
    }
}

function getLogin() {
    var userInfos = {
        email: document.getElementById("email").value,
        password: document.getElementById("password").value,
    };

    console.log(userInfos);

    //? Check if all fields are filled
    if (userInfos.email == "" || userInfos.password == "") {
        alert("Please fill in all fields");
        window.location.href = "../pageLogin.html";
    }

    xhr = getXmlHttpRequestObject();
    xhr.onreadystatechange = loginUser;
    // asynchronous requests
    xhr.open("POST", "http://localhost:6969/login-user", true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify(userInfos));
}