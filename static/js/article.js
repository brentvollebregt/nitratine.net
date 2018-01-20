var style = document.createElement("style");
document.head.appendChild(style);
sheet = style.sheet;
sheet.addRule('h1:before', 'background-image: url(/non-static' + window.location.pathname + '/icon.png)');

function rightSidebarCalculations() {
    if (window.innerWidth >= 1280) {
        // 280 nav, min 700 content, 300 right nav
        if (document.getElementsByClassName('article_content').length === 1) {
            var new_width = window.innerWidth - 580;
            document.getElementsByClassName('article_content')[0].style.maxWidth = new_width + 'px';
            document.getElementById('right_sidebar').style.display = 'block';
            document.getElementById('right_sidebar').style.marginLeft = (window.innerWidth - 300) + 'px';
        }
    } else {
        document.getElementsByClassName('article_content')[0].style.maxWidth = '1200px';
        document.getElementById('right_sidebar').style.display = 'none';
    }
}

window.addEventListener('load', function() {
    rightSidebarCalculations();
}, true);

window.addEventListener('resize', function(){
  rightSidebarCalculations();
});
