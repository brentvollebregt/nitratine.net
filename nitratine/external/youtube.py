from dataclasses import dataclass
from typing import List
import xml.etree.ElementTree as ET

import requests

from ..config import site_config


@dataclass
class YouTubeVideo:
    """ Summary of a YouTube video """
    id: str
    title: str
    href: str
    thumb_src: str


def __request_latest_youtube_videos(youtube_channel_id: str, max_results=6) -> List[YouTubeVideo]:
    """
    Get the latest videos for a YouTube channel
    max_results cannot exceed 15 (otherwise use the YouTube API)
    """
    request = requests.get(f'https://www.youtube.com/feeds/videos.xml?channel_id={youtube_channel_id}')
    assert request.status_code == 200

    root = ET.fromstring(request.content)
    namespace = {'': 'http://www.w3.org/2005/Atom', 'yt': 'http://www.youtube.com/xml/schemas/2015'}

    latest_videos = []
    for videoElement in root.findall('entry', namespace):
        video_id = videoElement.find('yt:videoId', namespace).text
        title = videoElement.find('title', namespace).text

        latest_videos.append(
            YouTubeVideo(
                video_id,
                title,
                f'https://www.youtube.com/watch?v={video_id}',
                f'https://img.youtube.com/vi/{video_id}/mqdefault.jpg',
            )
        )

    return latest_videos[:max_results]


__most_recent_youtube_videos_cache = None


def get_latest_youtube_videos() -> List[YouTubeVideo]:
    """ Get the cached most_recent_youtube_videos or make a request to get them and return them """
    global __most_recent_youtube_videos_cache

    if __most_recent_youtube_videos_cache is None:
        __most_recent_youtube_videos_cache = __request_latest_youtube_videos(
            youtube_channel_id=site_config.youtube_channel_id,
            max_results=6
        )

    return __most_recent_youtube_videos_cache
