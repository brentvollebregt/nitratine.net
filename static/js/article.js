var style = document.createElement("style");
document.head.appendChild(style);
sheet = style.sheet;
sheet.addRule('h1:before', 'background-image: url(/non-static' + window.location.pathname + '/icon.png)');

function sidebarSwitchesCheck() {
    // TODO Remove switches if they are over other links in sidebar
}

function rightSidebarCalculations() {
    // TODO Make a right sidebar
}

window.addEventListener('resize', function(event){
  sidebarSwitchesCheck();
  rightSidebarCalculations();
});

window.addEventListener('load', function() {
    sidebarSwitchesCheck();
    rightSidebarCalculations();
}, true);