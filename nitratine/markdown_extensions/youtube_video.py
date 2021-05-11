from xml.etree.ElementTree import Element, SubElement

from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern


class YouTubeVideoPattern(Pattern):
    """
    Matches `youtube:<video_id>` and converts to elements to render the associated YouTube video
    Modified from: https://github.com/Python-Markdown/github-links/blob/master/mdx_gh_links.py
    """
    ANCESTOR_EXCLUDES = ('a',)

    def __init__(self, md):
        super(YouTubeVideoPattern, self).__init__(r'youtube:([^"&?\/\s]{11})', md)

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
    def extendMarkdown(self, md):
        md.inlinePatterns.register(YouTubeVideoPattern(md), 'youtube-video', 100)
