"""
Functions for external (to posts) and easily separable calls
"""

import requests


def get_most_recent_youtube_videos(youtube_data_api_key: str, youtube_channel_id: str, max_results=6):
    requested_videos = requests.get(
        f'https://www.googleapis.com/youtube/v3/search?key={youtube_data_api_key}&channelId={youtube_channel_id}&part=id&order=date&maxResults={max_results}&type=video'
    ).json()['items']

    recent_videos = []
    for video in requested_videos:
        if 'videoId' not in video['id']:
            continue
        recent_videos.append({
            'thumb_src': f'https://img.youtube.com/vi/{video["id"]["videoId"]}/mqdefault.jpg',
            'href': f'https://www.youtube.com/watch?v={video["id"]["videoId"]}'
        })

    return recent_videos


def get_github_user_repos(github_username: str):
    github_repos_request = requests.get(f'https://api.github.com/users/{github_username}/repos')
    github_repos_request_data = github_repos_request.json()
    available_repos = sorted(
        github_repos_request_data,
        key=lambda x: x['stargazers_count'],
        reverse=True
    )
    return available_repos
