"""
Source: https://github.com/RickTalken/kbdextension
Copied into source as the source repo does not have much activity

MIT License

Copyright (c) 2020 Rick Talken

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern
import xml.etree.ElementTree as etree


class KbdPattern(Pattern):
    def __init__(self, pattern, md=None, css=None):
        self.css = css
        super().__init__(pattern, md)

    def handleMatch(self, m):
        """
        Accepts a match object and returns an ElementTree element of a plain
        Unicode string representation of the HTML <kbd> tag.
        """
        element = etree.Element("kbd")
        if self.css:
            element.set("class", self.css)
        element.text = m.group(3)
        return element


KBD_BRACKETS_RE = r"(\[\[)(.*?)(\]\])"
KBD_BRACES_RE = r"(\{\{)(.*?)(\}\})"
KBD_PARENS_RE = r"(\(\()(.*?)(\)\))"


class KbdExtension(Extension):
    """
    Manage configuration options for the KBD markdown extension and attach
    patterns for each configured Markdown syntactical element.
    """

    def __init__(self, **kwargs):
        # Define config options and defaults
        self.config = {
            "enable_brackets": [True, "Enable bracket syntax."],
            "brackets_css": ["", "Add custom CSS class for bracket syntax."],
            "enable_braces": [False, "Enable curly brace syntax."],
            "braces_css": ["", "Add custom CSS class for brace syntax."],
            "enable_parens": [False, "Enable parenthesis syntax."],
            "parens_css": ["", "Add custom CSS class for parenthesis syntax."],
        }
        # Call the parent class's __init__ method to configure options
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        if self.getConfig("enable_brackets"):
            brackets_css = self.getConfig("brackets_css")
            kbd_brackets_pattern = (
                KbdPattern(KBD_BRACKETS_RE, css=brackets_css)
                if brackets_css
                else KbdPattern(KBD_BRACKETS_RE)
            )
            md.inlinePatterns.register(kbd_brackets_pattern, "kbd-brackets", 201)
        if self.getConfig("enable_braces"):
            braces_css = self.getConfig("braces_css")
            kbd_braces_pattern = (
                KbdPattern(KBD_BRACES_RE, css=braces_css)
                if braces_css
                else KbdPattern(KBD_BRACES_RE)
            )
            md.inlinePatterns.register(kbd_braces_pattern, "kbd-braces", 202)
        if self.getConfig("enable_parens"):
            parens_css = self.getConfig("parens_css")
            kbd_parens_pattern = (
                KbdPattern(KBD_PARENS_RE, css=parens_css)
                if parens_css
                else KbdPattern(KBD_PARENS_RE)
            )
            md.inlinePatterns.register(kbd_parens_pattern, "kbd-parens", 203)


def makeExtension(**kwargs):
    """
    Return an instance of the KBD Python-Markdown extension.
    This method enables the extension for use in MkDocs.
    """
    return KbdExtension(**kwargs)
