from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern
from markdown.treeprocessors import Treeprocessor

from xml.etree.ElementTree import Element, SubElement


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


class HeaderLinkProcessor(Treeprocessor):
    SUPPORTED_ELEMENTS = ['h2', 'h3', 'h4', 'h5', 'h6']
    SVG_ICON_PATH = 'M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z'

    def run(self, root):
        for element in root:
            if element.tag in self.SUPPORTED_ELEMENTS:
                # Get the children from the header tag and remove them
                original_header_children = list(element)
                for e in original_header_children:
                    element.remove(e)

                # Add a wrapper so we can keep using :target::before on the header
                span_wrapper = SubElement(element, 'span')
                span_wrapper.set('style', 'position:relative')

                # Put an `a` tag in this wrapper and then the original content from the header
                link_element = SubElement(span_wrapper, 'a')
                for e in original_header_children:
                    span_wrapper.append(e)

                # Put the original text in the header after the new `a` tag then remove the text from the header
                link_element.tail = element.text
                element.text = '\n'

                # Setup the rest of the `a` tag (the clickable anchor)
                link_element.set('class', 'anchor')
                link_element.set('href', f'#{element.get("id")}')

                # Setup the internal SVG
                svg_element = SubElement(link_element, 'svg')
                svg_element.set('aria-hidden', 'true')
                svg_element.set('focusable', 'false')
                svg_element.set('height', '16')
                svg_element.set('width', '16')
                svg_element.set('version', '1.1')
                svg_element.set('viewBox', '0 0 16 16')
                path_element = SubElement(svg_element, 'path')
                path_element.set('fill-rule', 'evenodd')
                path_element.set('d', self.SVG_ICON_PATH)


class HeaderLinkExtension(Extension):
    def extendMarkdown(self, md):
        md.treeprocessors.register(HeaderLinkProcessor(md), 'headerlinkprocessor', 1)
