function doSearch(inputElement) {
    window.location.href = searchUrl + '?q=' + encodeURIComponent(inputElement.value);
}

const sidebarSearchInput = document.getElementById('sidebar-search');
const sidebarSearchButton = document.getElementById('sidebar-search-submit');
const searchPageSearchInput = document.getElementById('search');

sidebarSearchButton.addEventListener('click', function () { doSearch(sidebarSearchInput); });
sidebarSearchInput.addEventListener('keyup', function (e) {
    e.preventDefault();
    if ((e.keyCode ? e.keyCode : e.which) === 13) {
        doSearch(sidebarSearchInput);
    }
});
searchPageSearchInput.addEventListener('keyup', function (e) {
    e.preventDefault();
    if ((e.keyCode ? e.keyCode : e.which) === 13) {
        doSearch(searchPageSearchInput);
    }
});
