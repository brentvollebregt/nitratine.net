delete_article = function () {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/admin/article/delete', true);
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
    xhr.open("POST", '/admin/article/upload', true);
    var formData = new FormData();
    formData.append('sub', document.getElementById('upload_article_sub').value);
    formData.append('article', document.getElementById('upload_article_url').value);
    formData.append('file', document.getElementById('upload_article_file').files[0]);
    xhr.upload.addEventListener("progress", function(e) {
        var percent = e.loaded / e.total;
        document.getElementById('upload_article_btn').textContent = Math.round(percent * 100) + "%";
    }, false);
    xhr.onreadystatechange = function(e) {
        if (xhr.readyState === 4) {
            document.getElementById('upload_article_btn').textContent = 'Upload';
        }
    };
    xhr.send(formData);
    xhr.onload = function () {
        success_message(JSON.parse(this.responseText)['success']);
        if (JSON.parse(this.responseText)['success']) {
            document.getElementById('upload_article_url').value = '';
            document.getElementById('upload_article_file').value = '';
        }
    };
};

move_article = function () {
    var sub = document.getElementById('move_article_sub_from').value;
    var article = document.getElementById('move_article_url').value;
    var to_sub = document.getElementById('move_article_sub_to').value;
    var redirect = document.getElementById('move_article_redirect').checked;
    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/admin/article/move', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.overrideMimeType('application/json');
    xhr.send(JSON.stringify({
        sub: sub,
        article: article,
        to_sub: to_sub,
        redirect: redirect
    }));
    xhr.onload = function () {
        success_message(JSON.parse(this.responseText)['success']);
    };
};

upload_json = function () {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/admin/json/upload', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.overrideMimeType('application/json');
    xhr.send(JSON.stringify({
        data: JSON.parse(document.getElementById('jsonEdit').value)
    }));
    xhr.onload = function () {
        success_message(JSON.parse(this.responseText)['success']);
    };
};

download_json = function () {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", '/admin/json/download', true);
    xhr.overrideMimeType('application/json');
    xhr.send(null);
    xhr.onload = function () {
        document.getElementById('jsonEdit').value = JSON.stringify(JSON.parse(this.responseText)['data']);
        success_message(JSON.parse(this.responseText)['success']);
    };
};

add_redirect = function () {
    var from = document.getElementById('redirect_from').value;
    var to = document.getElementById('redirect_to').value;
    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/admin/redirects/add', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.overrideMimeType('application/json');
    xhr.send(JSON.stringify({
        from: from,
        to: to
    }));
    xhr.onload = function () {
        success_message(JSON.parse(this.responseText)['success']);
    };
};

remove_redirect = function () {
    var redirect = document.getElementById('redirect_remove').value;
    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/admin/redirects/remove', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.overrideMimeType('application/json');
    xhr.send(JSON.stringify({
        redirect: redirect
    }));
    xhr.onload = function () {
        success_message(JSON.parse(this.responseText)['success']);
    };
};

modify_desc = function (page) {
    var desc = document.getElementById('staticDesc_' + page).value;
    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/admin/modify_description/'+ page, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.overrideMimeType('application/json');
    xhr.send(JSON.stringify({
        desc: desc
    }));
    xhr.onload = function () {
        success_message(JSON.parse(this.responseText)['success']);
    };
};

set_push_per_view = function (enable) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/admin/set_push_per_view', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.overrideMimeType('application/json');
    xhr.send(JSON.stringify({
        enable: enable
    }));
    xhr.onload = function () {
        success_message(JSON.parse(this.responseText)['success']);
        if (JSON.parse(this.responseText)['success']) {
            if (enable) {
                document.getElementById('ppv_on').style.background = '#d81b60';
                document.getElementById('ppv_off').style.background = '';
            } else {
                document.getElementById('ppv_on').style.background = '';
                document.getElementById('ppv_off').style.background = '#d81b60';
            }
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

upload_article_folder = function () {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/admin/article_folder/upload', true);
    var formData = new FormData();
    formData.append('file', document.getElementById('article_folder_zip').files[0]);
    xhr.upload.addEventListener("progress", function(e) {
        var percent = e.loaded / e.total;
        document.getElementById('article_folder_upload_btn').textContent = Math.round(percent * 100) + "%";
    }, false);
    xhr.onreadystatechange = function(e) {
        if (xhr.readyState === 4) {
            document.getElementById('article_folder_upload_btn').textContent = 'Upload';
        }
    };
    xhr.send(formData);
    xhr.onload = function () {
        success_message(JSON.parse(this.responseText)['success']);
        if (JSON.parse(this.responseText)['success']) {
            document.getElementById('article_folder_zip').value = '';
        }
    };
};
