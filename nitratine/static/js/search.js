function doSearch() {
    let query = document.getElementById('search').value;
    window.location.href = searchUrl + '?q=' + encodeURIComponent(query);
}

document.getElementById('search-submit').addEventListener('click', function () {
    doSearch();
});
document.getElementById('search').addEventListener('keyup', function (e) {
    e.preventDefault();
    if ((e.keyCode ? e.keyCode : e.which) === 13) {
        doSearch();
    }
});