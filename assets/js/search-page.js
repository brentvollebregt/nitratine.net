function search() {
    let query = document.getElementById('search').value;
    if (query !== '') {

        // Prepare scores
        let scores = {};
        Object.keys(site_content).map(function(key) { scores[key] = 0; });

        // Get the part of the query
        let query_parts = query.split(' ')
            .map(x => x.toLowerCase()) // Make lowercase
            .filter(function(x) {if (x !== '') {return x;}}); // Remove empty strings

        // Add points to scores based off matches
        Object.keys(site_content).forEach(function (post) {
            let title = site_content[post]['title'].toLowerCase();
            let category = site_content[post]['category'].toLowerCase();
            let description = site_content[post]['description'].toLowerCase();
            let tags = site_content[post]['tags'].map(x => x.toLowerCase());

            // Score each match
            query_parts.forEach(function (query_part) {
                let query_part_re = new RegExp(query_part, "g");
                scores[post] += (title.match(query_part_re) || []).length * 3;
                scores[post] += (category.match(query_part_re) || []).length * 2;
                scores[post] += (description.match(query_part_re) || []).length;
                if (tags.includes(query_part)) {
                    scores[post] += 2;
                }
            })
        });

        // Sort posts
        let scores_no_0 = Object.keys(scores).filter(function (x) { if (scores[x] !== 0) {return x;} }); // Remove all 0 scores
        let scores_sorted = scores_no_0.sort(function (a,b) {return scores[b] - scores[a];});
        let scores_top_10 = scores_sorted.slice(0, 10);

        // Display results
        let results = document.getElementById('results');
        // Clear current results
        while (results.firstChild) {
            results.removeChild(results.firstChild);
        }
        // Construct new results
        scores_top_10.forEach(function (search_result) {
            let tmp_wrapper = document.createElement('div');

                let title = document.createElement('h3');
                title.classList.add('mb-0');
                    let title_link = document.createElement('a');
                    title_link.href = '/blog/post/' + search_result;
                    title_link.innerText = site_content[search_result]['title'];
                    title.appendChild(title_link);
                tmp_wrapper.appendChild(title);

                let specifics = document.createElement('p');
                specifics.classList.add('text-muted');
                specifics.classList.add('mb-0');
                    let date = document.createElement('a');
                    date.classList.add('text-muted');
                    date.href = '/blog/archive/#' + new Date(site_content[search_result]['date']).getFullYear();
                    date.innerText = site_content[search_result]['date'].substring(5, 16);
                    specifics.appendChild(date);
                    let category = document.createElement('a');
                    category.classList.add('badge');
                    category.classList.add('badge-primary');
                    category.classList.add('ml-2');
                    category.href = '/blog/categories/#' + site_content[search_result]['category'];
                    category.innerText = site_content[search_result]['category'];
                    specifics.appendChild(category);
                    site_content[search_result]['tags'].forEach(function (tag) {
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
                description.innerText = site_content[search_result]['description'];
                tmp_wrapper.appendChild(description);

            results.appendChild(tmp_wrapper);
        });

    }
}

function read_query() {
    let url = new URL(window.location.href);
    let query = url.searchParams.get('q');
    if (query !== null) {
        document.getElementById('search').value = query;
        search();
    }
}

document.getElementById('search-submit').addEventListener('click', function () {
    search();
});
document.getElementById('search').addEventListener('keyup', function (e) {
    e.preventDefault();
    if ((e.keyCode ? e.keyCode : e.which) === 13) {
        search();
    }
});
read_query();