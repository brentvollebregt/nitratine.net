login = function () {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/admin", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        username: username,
        password: password
    }));
    xhr.onload = function () {
        var data = JSON.parse(this.responseText)['success'];
        if (data) {
            window.location.reload();
        } else {
            document.getElementById('username').value = '';
            document.getElementById('password').value = '';
        }
    };
};

logout = function () {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/admin/logout", true);
    xhr.send(null);
    xhr.onload = function () {
        window.location.reload();
    };
};