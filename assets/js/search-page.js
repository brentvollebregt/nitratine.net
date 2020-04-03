function search() {
    const resultsNode = document.getElementById('results');

    // Get search query
    let query = document.getElementById('search').value;
    if (query !== '' && query !== undefined) {
        // Find top 10 results
        site_content.map(item => item.meta.concatenated_tags = item.meta.tags.join(' '));
        fuzzysort.goAsync(query, site_content, {
            threshold: -1000,
            limit: 10,
            allowTypo: true,
            keys: ['path', 'meta.category', 'meta.description', 'meta.concatenated_tags', 'meta.title'],
        })
            .then(searchResults => {
                // Clear current results
                clearResults(resultsNode);

                // It seems that fuzzysort can return duplicate results (e.g. when searching "spotify" on this site)
                const uniqueSearchResults = searchResults.filter(
                    (value, index, self) => self.indexOf(self.find(v => v.path === value.path)) !== index
                );

                // Show the results
                uniqueSearchResults.forEach(result => displayResult(result.obj, resultsNode));
            });
    } else {
        clearResults(resultsNode);
    }
}

function clearResults(resultsNode) {
    while (resultsNode.firstChild) {
        resultsNode.removeChild(resultsNode.firstChild);
    }
}

function displayResult(result, rootResultsNode) {
    let tmp_wrapper = document.createElement('div');

    let title = document.createElement('h3');
    title.classList.add('mb-0');
    let title_link = document.createElement('a');
    title_link.href = '/blog/post/' + result.path;
    title_link.innerText = result.meta.title;
    title.appendChild(title_link);
    tmp_wrapper.appendChild(title);

    let specifics = document.createElement('p');
    specifics.classList.add('text-muted');
    specifics.classList.add('mb-0');
    let date = document.createElement('a');
    date.classList.add('text-muted');
    date.href = '/blog/archive/#' + new Date(result.meta.date).getFullYear();
    date.innerText = result.meta.date.substring(5, 16);
    specifics.appendChild(date);
    let category = document.createElement('a');
    category.classList.add('badge');
    category.classList.add('badge-primary');
    category.classList.add('ml-2');
    category.href = '/blog/categories/#' + result.meta.category;
    category.innerText = result.meta.category;
    specifics.appendChild(category);
    result.meta.tags.forEach(function (tag) {
        let tmp_tag = document.createElement('a');
        tmp_tag.classList.add('badge');
        tmp_tag.classList.add('badge-warning');
        tmp_tag.classList.add('ml-1');
        tmp_tag.href = '/blog/tags/#' + tag;
        tmp_tag.innerText = tag;
        specifics.appendChild(tmp_tag);
    });
    tmp_wrapper.appendChild(specifics);

    let description = document.createElement('p');
    description.innerText = result.meta.description;
    tmp_wrapper.appendChild(description);

    rootResultsNode.appendChild(tmp_wrapper);
}

// Setup search listener
document.getElementById('search').addEventListener('keyup', function () {
    search();
});

// Read query string
let url = new URL(window.location.href);
let query = url.searchParams.get('q');
if (query !== null) {
    document.getElementById('search').value = query;
    search();
}
