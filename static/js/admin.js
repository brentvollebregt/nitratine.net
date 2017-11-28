login = function () {
    var username = '';
    var password = '';
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