var style = document.createElement("style");
document.head.appendChild(style);
sheet = style.sheet;
sheet.addRule('h1:before', 'background-image: url(/non-static' + window.location.pathname + '/icon.png)');

function rightSidebarCalculations() {
    // TODO Make a right sidebar
    // Check that the nav bar is showing
    // Make sure there is div.article_content for main content
    // Check that there is reasonable space for the section (test this to find thee width)
    // Calculate and set new size of content
    // Make right sidebar visible (300px wide; same as nav)
}

window.addEventListener('load', function() {
    rightSidebarCalculations();
}, true);

window.addEventListener('resize', function(){
  rightSidebarCalculations();
});
