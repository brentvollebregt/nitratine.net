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

upload_json = function () {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/admin/upload_json', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.overrideMimeType('application/json');
    xhr.send(JSON.stringify({
        data: document.getElementById('jsonEdit').value
    }));
    xhr.onload = function () {
        console.log(JSON.parse(this.responseText)['success']);
    };
};

download_json = function () {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", '/admin/download_json', true);
    xhr.overrideMimeType('application/json');
    xhr.send(null);
    xhr.onload = function () {
        console.log(JSON.parse(this.responseText)['success']);
        console.log(JSON.parse(this.responseText)['data']);
        document.getElementById('jsonEdit').value = JSON.stringify(JSON.parse(this.responseText)['data']);
    };
};

export_stats = function () {

};

delete_article = function () {

};

upload_article = function () {

};

simple_call = function (url) {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    xhr.overrideMimeType('application/json');
    xhr.send(null);
    xhr.onload = function () {
        console.log(JSON.parse(this.responseText)['success']);
    };
};
