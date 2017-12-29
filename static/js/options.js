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


getThemeToSwitch();
getSnowToSwitch();