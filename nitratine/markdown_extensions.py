import base64
from xml.etree.ElementTree import Element, SubElement

from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern
from markdown.treeprocessors import Treeprocessor

from .config import POST_SOURCE
from .utils import get_resized_image, guess_rendered_size


class YouTubeVideoPattern(Pattern):
    """
    Matches `youtube:<video_id>` and converts to elements to render the associated YouTube video
    Modified from: https://github.com/Python-Markdown/github-links/blob/master/mdx_gh_links.py
    """
    ANCESTOR_EXCLUDES = ('a',)

    def __init__(self, config, md):
        MENTION_RE = r'youtube:([^"&?\/\s]{11})'
        super(YouTubeVideoPattern, self).__init__(MENTION_RE, md)
        self.config = config

    def handleMatch(self, m):
        video_id = m.group(2)

        root = Element('div')
        root.set('class', 'embedded_yt my-3')

        wrapper_element = SubElement(root, 'div')

        iframe = SubElement(wrapper_element, 'iframe')
        iframe.set('allow', 'autoplay; encrypted-media')
        iframe.set('allowfullscreen', '')
        iframe.set('src', f'https://www.youtube.com/embed/{video_id}')

        return root


class YouTubeVideoExtension(Extension):
    def __init__(self, *args, **kwargs):
        self.config = {}
        super(YouTubeVideoExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns['youtube-video'] = YouTubeVideoPattern(self.getConfigs(), md)


class LazySizesImageProcessor(Treeprocessor):
    def run(self, root):
        for element in root.iter('img'):
            src = element.get('src')
            if src.startswith('/posts/'):
                # Identify file
                file = POST_SOURCE / src[len('/posts/'):]
                # Get the resized image, convert it to b64 and then guess the render dimensions (~790 post with space)
                resized_image = get_resized_image(file, 15)
                image_bs4 = base64.b64encode(resized_image.image_bytes)
                display_size_guess = guess_rendered_size(resized_image.original_size, 790)
                # Setup img tag
                element.set('class', 'lazyload blur-up')
                element.set('data-src', element.get('src'))
                element.set('src', f"data:image/png;base64, {image_bs4.decode()}")
                element.set('style', f"width: {display_size_guess[0]}px; height: {display_size_guess[1]}px;")


class LazySizesImageExtension(Extension):
    def extendMarkdown(self, md):
        md.treeprocessors.register(LazySizesImageProcessor(md), 'inlineimageprocessor', 15)
