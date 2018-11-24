document.getElementById('search-submit').addEventListener('click', function () {
    let query = document.getElementById('search').value;
    window.location.href = searchUrl + '?q=' + encodeURIComponent(query);
});
