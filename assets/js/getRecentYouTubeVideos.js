/**
 * Will append 6 most recent youtube videos
 */

(function () {
    // let youtube_data_api_key = '';
    // let youtube_channel_id = '';
    let xhr = new XMLHttpRequest();
    xhr.open("GET", 'https://www.googleapis.com/youtube/v3/search?key=' + youtube_data_api_key + '&channelId=' + youtube_channel_id + '&part=id&order=date&maxResults=6&type=video', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.overrideMimeType('application/json');
    xhr.send();
    xhr.onload = function () {
        let data = JSON.parse(this.responseText)['items'];
        let parent = document.getElementById('recent-yt-videos');

        for (let i = 0; i < data.length; i++) {
            if (data[i]['id']['videoId'] === undefined) {continue}
            let tmp_node = document.createElement('img');
            tmp_node.src = 'https://img.youtube.com/vi/' + data[i]['id']['videoId'] + '/mqdefault.jpg';
            tmp_node.href = 'https://www.youtube.com/watch?v=' + data[i]['id']['videoId'];
            tmp_node.onclick = function () { window.open(this.href, '_blank') };
            parent.appendChild(tmp_node);
        }

        if (data === undefined) {
            parent.innerText = 'An error occurred';
        }
    }
}());