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

delete_article = function () {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/admin/delete_article', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.overrideMimeType('application/json');
    xhr.send(JSON.stringify({
        sub: document.getElementById('delete_article_sub').value,
        url: document.getElementById('delete_article_url').value
    }));
    xhr.onload = function () {
        console.log(JSON.parse(this.responseText)['success']);
        document.getElementById('delete_article_sub').value = '';
        document.getElementById('delete_article_url').value = '';
    };
};

upload_article = function () {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/admin/upload_article', true);
    var formData = new FormData();
    formData.append('sub', document.getElementById('upload_article_sub').value);
    formData.append('url', document.getElementById('upload_article_url').value);
    formData.append('file', document.getElementById('upload_article_file').files[0]);
    xhr.send(formData);
    xhr.onload = function () {
        console.log(JSON.parse(this.responseText)['success']);
    };
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
