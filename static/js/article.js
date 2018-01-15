var style = document.createElement("style");
document.head.appendChild(style);
sheet = style.sheet;
sheet.addRule('h1:before', 'background-image: url(/non-static' + window.location.pathname + '/icon.png)');

function rightSidebarCalculations() {
    // TODO Make a right sidebar
}

window.addEventListener('load', function() {
    rightSidebarCalculations();
}, true);

window.addEventListener('resize', function(){
  rightSidebarCalculations();
});
