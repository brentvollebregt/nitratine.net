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

