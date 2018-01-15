toggleNav = function (navigation_bar) {
    document.getElementById('small_nav_icon');
    var nav_icon = document.getElementById('small_nav_icon');
    var navDropped = true;
    if (nav_icon.dropped == null || nav_icon.dropped == false) {
        navDropped = false;
    }

    var setDisplay = 'block';
    if (navDropped) {
        nav_icon.style.transform = "";
        setDisplay = 'none';
    } else {
        nav_icon.style.transform = "rotate(180deg)";
    }

    var children = navigation_bar.children;
    for (var i = 0; i < children.length; i++) {
        if (children[i].classList.contains('small_nav_item')) {
            children[i].style.display = setDisplay
        }
    }

    nav_icon.dropped = !navDropped
};

linkTo = function (location) {
    window.location.href = "/" + location;
};

navToggle = function () {
    var nav_icon = document.getElementById('phone_nav_bar_icon');
    var phone_nav = document.getElementById('phone_nav');

    var navDropped = true;
    if (nav_icon.dropped == null || nav_icon.dropped == false) {
        navDropped = false;
    }

    if (navDropped) {
        // nav_bar.style.marginTop = "0px";
        nav_icon.style.transform = "";
        phone_nav.style.marginTop = "-408px"
    } else {
        // nav_bar.style.marginTop = "408px";
        nav_icon.style.transform = "rotate(180deg)";
        phone_nav.style.marginTop = "0px"
    }

    nav_icon.dropped = !navDropped
};

function checkOptionsSection() {
    var nav_options = document.getElementById('nav_options');
    var last_nav_link = document.getElementById('last_nav_link');
    console.log(last_nav_link.getBoundingClientRect().bottom  + ' ' + nav_options.getBoundingClientRect().top);
    console.log(last_nav_link.getBoundingClientRect().bottom >= nav_options.getBoundingClientRect().top);
    if (last_nav_link.getBoundingClientRect().bottom >= nav_options.getBoundingClientRect().top) {
        nav_options.style.visibility = 'hidden';
    } else {
        nav_options.style.visibility = 'visible';
    }
}

window.addEventListener('load', function () {
    checkOptionsSection();
}, true);

window.addEventListener('resize', function () {
    checkOptionsSection();
});