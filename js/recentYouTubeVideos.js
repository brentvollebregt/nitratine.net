/**
 * [recentYouTubeVideos]
 * Will append 3 or 2 (depending on size) most recent youtube videos i
 */
(function () {
    let items = 3;
    if (window.innerWidth <= 770) {
        let items = 2;
    }

    let xhr = new XMLHttpRequest();
    xhr.open("GET", 'https://www.googleapis.com/youtube/v3/search?key=' + youtube_data_API_key + '&channelId=' + youtube_channel_id + '&part=id&order=date&maxResults=' + items + '&type=video', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.overrideMimeType('application/json');
    xhr.send();
    xhr.onload = function () {
        let data = JSON.parse(this.responseText)['items'];
        let parent = document.getElementById('recentVideos');

        for (let i = 0; i < data.length; i++) {
            if (data[i]['id']['videoId'] === undefined) {continue}
            let tmp_node = document.createElement('img');
            tmp_node.src = 'https://img.youtube.com/vi/' + data[i]['id']['videoId'] + '/mqdefault.jpg';
            tmp_node.style.width = '100%';
            tmp_node.style.height = 'auto';
            tmp_node.style.marginBottom = '1px';
            tmp_node.href = 'https://www.youtube.com/watch?v=' + data[i]['id']['videoId'];
            tmp_node.onclick = function () { window.open(this.href, '_blank') };
            tmp_node.style.cursor = 'pointer';
            parent.appendChild(tmp_node);
        }

        document.getElementById('recentVideosSide').style.display = 'block';
    }
}());
