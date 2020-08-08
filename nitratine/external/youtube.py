from dataclasses import dataclass
from typing import List

import requests

from ..config import site_config


@dataclass
class YouTubeVideo:
    """ Summary of a YouTube video """
    href: str
    thumb_src: str


def __request_for_most_recent_youtube_videos(
        youtube_data_api_key: str,
        youtube_channel_id: str,
        max_results=6) -> List[YouTubeVideo]:
    """ Get the most recent videos for a YouTube channel """
    requested_videos = requests.get(
        f'https://www.googleapis.com/youtube/v3/search?key={youtube_data_api_key}&channelId={youtube_channel_id}&part=id&order=date&maxResults={max_results}&type=video'
    ).json()['items']

    recent_videos = [
        YouTubeVideo(
            f'https://www.youtube.com/watch?v={v["id"]["videoId"]}',
            f'https://img.youtube.com/vi/{v["id"]["videoId"]}/mqdefault.jpg',
        )
        for v in requested_videos
        if 'videoId' in v['id']
    ]

    return recent_videos


__most_recent_youtube_videos_cache = None


def get_most_recent_youtube_videos() -> List[YouTubeVideo]:
    """ Get the cached most_recent_youtube_videos or make a request to get them and return them """
    global __most_recent_youtube_videos_cache

    if __most_recent_youtube_videos_cache is None:
        __most_recent_youtube_videos_cache = __request_for_most_recent_youtube_videos(
            youtube_data_api_key=site_config.youtube_data_api_key,
            youtube_channel_id=site_config.youtube_channel_id,
            max_results=6
        )

    return __most_recent_youtube_videos_cache
