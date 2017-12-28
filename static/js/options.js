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
};

setThemeLight = function () {
    localStorage.removeItem("dark_theme");
    document.getElementById("dark_theme_switch").checked = false;
    setCSSDisabled('css_dark_theme', true);
    setCSSDisabled('css_light_theme', false);
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
    document.getElementById("snow").classList.add("snow")
};

setSnowFalse = function () {
    localStorage.removeItem("snow");
    document.getElementById("snow_switch").checked = false;
    document.getElementById("snow").classList.remove("snow")
};


getThemeToSwitch();
getSnowToSwitch();