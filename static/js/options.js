// Theme
getThemeToSwitch = function () {
    if (localStorage.getItem("dark_theme") !== null) {
        setThemeDark();
    } else {
        setThemeLight();
    }
};

setTheme = function () {
    console.log("Set Theme");
    if (localStorage.getItem("dark_theme") === null) {
        setThemeDark();
    } else {
        setThemeLight();
    }

};

setThemeDark = function () {
    localStorage.setItem("dark_theme", true);
    document.getElementById("dark_theme_switch").checked = true;
    // Disable light if exists
    // Enable dark if exists
    // Create dark if not
};

setThemeLight = function () {
    localStorage.removeItem("dark_theme");
    document.getElementById("dark_theme_switch").checked = false;
    // Disable dark theme if exists
    // Enable light if exists
    // Create light if not
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