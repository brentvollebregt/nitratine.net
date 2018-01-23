// Links
linkTo = function (location) {
    window.location.href = "/" + location;
};

// Small screen navigation
navToggle = function () {
    var nav_icon = document.getElementById('phone_nav_bar_icon');
    var phone_nav = document.getElementById('phone_nav');

    var navDropped = true;
    if (nav_icon.dropped == null || nav_icon.dropped == false) {
        navDropped = false;
    }

    if (navDropped) {
        nav_icon.style.transform = "";
        phone_nav.style.marginTop = "-408px"
    } else {
        nav_icon.style.transform = "rotate(180deg)";
        phone_nav.style.marginTop = "0px"
    }

    nav_icon.dropped = !navDropped
};

// Right Sidebar
function checkRightSidebar() {
    if (window.innerWidth >= 1790 && enable_right_sidebar) {
        // Navbar 280, Home and Sub content max 1200, right sidebar 300 + 10 margin (should be 15 but we'll support more)
        document.getElementById('right_sidebar').style.display = 'flex';
    } else {
        document.getElementById('right_sidebar').style.display = 'none';
    }
}

function setupRightSidebar() {
    // Stats on videos: https://www.googleapis.com/youtube/v3/videos?part=statistics&id=#&key=#
    var xhr = new XMLHttpRequest();
    xhr.open("GET", 'https://www.googleapis.com/youtube/v3/search?key=' + youtube_data_API_key + '&channelId=' + youtube_channel_id + '&part=id&order=date&maxResults=6&type=video', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.overrideMimeType('application/json');
    xhr.send();
    xhr.onload = function () {
        var data = JSON.parse(this.responseText)['items'];
        var ids = [];
        var parent = document.getElementById('recent-yt');
        for (var i = 0; i < data.length; i++) {
            if (data[i]['id']['videoId'] === undefined) {continue}
            ids.push(data[i]['id']['videoId']);
            var tmp_node = document.createElement('img');
            tmp_node.src = 'https://img.youtube.com/vi/' + data[i]['id']['videoId'] + '/mqdefault.jpg';
            tmp_node.style.width = '100%';
            tmp_node.style.height = 'auto';
            tmp_node.href = 'https://www.youtube.com/watch?v=' + data[i]['id']['videoId'];
            tmp_node.onclick = function () { window.open(this.href, '_blank') };
            tmp_node.style.cursor = 'pointer';
            parent.appendChild(tmp_node);
        }
        var yt_text = document.createElement('div');
        yt_text.id = 'recent_yt_videos';
        yt_text.innerText = 'Recent YouTube Videos';
        yt_text.style.textAlign = 'center';
        yt_text.style.fontSize = '12px';
        parent.parentNode.insertBefore(yt_text, parent);
    };
}

// Options view in sidebar
function checkOptionsSection() {
    var nav_options = document.getElementById('nav_options');
    var last_nav_link = document.getElementById('last_nav_link');
    if (last_nav_link.getBoundingClientRect().bottom >= nav_options.getBoundingClientRect().top) {
        nav_options.style.visibility = 'hidden';
    } else {
        nav_options.style.visibility = 'visible';
    }
}

// Theme
getThemeToSwitch = function () {
    if (localStorage.getItem("dark_theme") !== null) {
        setThemeDark();
    } else {
        setThemeLight();
    }
};

setTheme = function () {
    if (localStorage.getItem("dark_theme") === null) {
        setThemeDark();
    } else {
        setThemeLight();
    }
};

setThemeDark = function () {
    localStorage.setItem("dark_theme", true);
    document.getElementById("dark_theme_switch").checked = true;
    setCSSDisabled('css_dark_theme', false);
    setCSSDisabled('css_light_theme', true);

    var phone_nav = document.getElementById('phone_nav_theme');
    var phone_nav_img = phone_nav.getElementsByTagName('img')[0];
    var phone_nav_text = phone_nav.getElementsByTagName('div')[0];
    phone_nav_img.src = "/img/dark-icon_enabled.svg";
    phone_nav_text.style.color = '#d81b60';
};

setThemeLight = function () {
    localStorage.removeItem("dark_theme");
    document.getElementById("dark_theme_switch").checked = false;
    setCSSDisabled('css_dark_theme', true);
    setCSSDisabled('css_light_theme', false);

    var phone_nav = document.getElementById('phone_nav_theme');
    var phone_nav_img = phone_nav.getElementsByTagName('img')[0];
    var phone_nav_text = phone_nav.getElementsByTagName('div')[0];
    phone_nav_img.src = "/img/dark-icon.svg";
    phone_nav_text.style.color = 'white';
};

setCSSDisabled = function (className, disabled) {
    var stylesheets = document.getElementsByClassName(className);
    for (var i = 0; i < stylesheets.length; i++) {
        stylesheets[i].disabled = disabled;
    }
};

// Snow
getSnowToSwitch = function () {
    if (localStorage.getItem("snow") !== null) {
        setSnowTrue();
    } else {
        setSnowFalse();
    }
};

setSnow = function () {
    if (localStorage.getItem("snow") === null) {
        setSnowTrue();
    } else {
        setSnowFalse();
    }
};

setSnowTrue = function () {
    localStorage.setItem("snow", true);
    document.getElementById("snow_switch").checked = true;
    document.getElementById("snow").classList.add("snow");

    var phone_nav = document.getElementById('phone_nav_snow');
    var phone_nav_img = phone_nav.getElementsByTagName('img')[0];
    var phone_nav_text = phone_nav.getElementsByTagName('div')[0];
    phone_nav_img.src = "/img/snow-icon_enabled.svg";
    phone_nav_text.style.color = '#d81b60';
};

setSnowFalse = function () {
    localStorage.removeItem("snow");
    document.getElementById("snow_switch").checked = false;
    document.getElementById("snow").classList.remove("snow");

    var phone_nav = document.getElementById('phone_nav_snow');
    var phone_nav_img = phone_nav.getElementsByTagName('img')[0];
    var phone_nav_text = phone_nav.getElementsByTagName('div')[0];
    phone_nav_img.src = "/img/snow-icon.svg";
    phone_nav_text.style.color = 'white';
};

// Events
window.addEventListener('resize', function () {
    checkOptionsSection();
    checkRightSidebar();
});

window.addEventListener('load', function () {
    setupRightSidebar();
});
