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
        success_message(JSON.parse(this.responseText)['success']);
    };
};

download_json = function () {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", '/admin/download_json', true);
    xhr.overrideMimeType('application/json');
    xhr.send(null);
    xhr.onload = function () {
        document.getElementById('jsonEdit').value = JSON.stringify(JSON.parse(this.responseText)['data']);
        success_message(JSON.parse(this.responseText)['success']);
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
        success_message(JSON.parse(this.responseText)['success']);
        if (JSON.parse(this.responseText)['success']) {
            document.getElementById('delete_article_sub').value = '';
            document.getElementById('delete_article_url').value = '';
        }
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
        success_message(JSON.parse(this.responseText)['success']);
        if (JSON.parse(this.responseText)['success']) {
            document.getElementById('upload_article_sub').value = '';
            document.getElementById('upload_article_url').value = '';
            document.getElementById('upload_article_file').value = '';
        }
    };
};

simple_call = function (url) {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    xhr.overrideMimeType('application/json');
    xhr.send(null);
    xhr.onload = function () {
        success_message(JSON.parse(this.responseText)['success']);
    };
};

success_message = function (success) {
    var success_node = document.getElementById('success');
    if (success) {
        success_node.style.background = '#25c725';
        success_node.textContent = 'Successful';
    } else {
        success_node.style.background = '#ff4343';
        success_node.textContent = 'Unsuccessful';
    }
    success_node.classList.remove('success_hide');
    window.setTimeout(
        function(){
            success_node.classList.add('success_hide')
        }, 3000
    );
};

cwd = function () {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", '/admin/cwd', true);
    xhr.overrideMimeType('application/json');
    xhr.send(null);
    xhr.onload = function () {
        if (JSON.parse(this.responseText)['success']) {
            alert(JSON.parse(this.responseText)['cwd'])
        }
    };
};
