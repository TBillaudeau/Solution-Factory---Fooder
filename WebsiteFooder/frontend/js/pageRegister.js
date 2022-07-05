var xhr = null;

getXmlHttpRequestObject = function () {
    if (!xhr) {
        // Create a new XMLHttpRequest object 
        xhr = new XMLHttpRequest();
    }
    return xhr;
};


function registerUser() {
    if (xhr.readyState == 4 && xhr.status == 200) {
        var response = xhr.responseText;
        if (response == "success") {
            alert("User successfully registered");
            window.location.href = "../pageLogin.html";
        } else {
            alert("User already exists");
            window.location.href = "../pageRegister.html";
        }
    }
}


function getRegister() {
    var userInfos = {
        firstName: document.getElementById("firstname").value,
        lastName: document.getElementById("lastname").value,
        birthdate: document.getElementById("birthdate").value,
        password: document.getElementById("password").value,
        confirmPassword: document.getElementById("passwordconfirmation").value,
        email: document.getElementById("email").value,
    };

    console.log(userInfos);

    //? Check if passwords match
    if (userInfos.password != userInfos.confirmPassword) {
        alert("Passwords do not match");
        window.location.href = "../pageRegister.html";
    }

    //? Check if all fields are filled
    if (userInfos.firstName === "" || userInfos.lastName === "" || userInfos.birthdate === "" || userInfos.email === "" || userInfos.password === "" || userInfos.confirmPassword === "") {
        alert("Please fill in all fields");
        window.location.href = "../pageRegister.html";
    }

    xhr = getXmlHttpRequestObject();
    xhr.onreadystatechange = registerUser;
    // asynchronous requests
    xhr.open("POST", "http://localhost:6969/register-user", true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify(userInfos));
}