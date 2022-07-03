var xhr = null;

getXmlHttpRequestObject = function () {
    if (!xhr) {
        // Create a new XMLHttpRequest object 
        xhr = new XMLHttpRequest();
    }
    return xhr;
};


function registerUser() {
    //? Get all the values from the form
    var firstName = document.getElementById("firstName").value;
    var lastName = document.getElementById("lastName").value;
    var birthdate = document.getElementById("birthdate").value;
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;
    var confirmPassword = document.getElementById("passwordconfirmation").value;

    //? Check if passwords match
    if (password !== confirmPassword) {
        alert("Passwords do not match");
        window.location.href = "pageRegister.html";
    }

    //? Check if all fields are filled
    if (firstName === "" || lastName === "" || birthdate === "" || email === "" || password === "" || confirmPassword === "") {
        alert("Please fill in all fields");
        window.location.href = "pageRegister.html";
    }

    //? Add the user to the database
    var xhr = getXmlHttpRequestObject();
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 201) {
            var response = xhr.responseText;
            if (response == "success") {
                alert("User successfully registered");
                window.location.href = "pageLogin.html";
            } else {
                alert("User already exists");
                window.location.href = "pageRegister.html";
            }
        }
    };
    xhr.open("POST", "http://localhost:6969/register-user", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({
        firstName: firstName,
        lastName: lastName,
        birthdate: birthdate,
        email: email,
        password: password
    }));

}