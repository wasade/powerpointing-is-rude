#!/usr/bin/env python

import re
from bipy.core.workflow import Workflow
from pyfiglet import figlet_format

from .formatters import attributes

attr_matchr = re.compile("(?P<attr>\[([^]]+)\])(?P<text>\(([^]]+)\))")

# requirements state checking methods
has_header = lambda x: 'header' in x
has_body = lambda x: 'body' in x
has_footer = lambda x: 'footer' in x

class PowerpointingIsRude(Workflow):
    def initialize_state(self, item):
        self.state = item

    @Workflow.method(priority=100)
    @Workflow.requires(state=has_header)
    def process_header(self):
        self._ascii_art_header()
        self._basic_header()

    @Workflow.method(priority=75)
    @Workflow.requires(state=has_body)
    def process_body(self):
        self.state['body'] = self._process_text(self.state['body'])

    @Workflow.method(priority=50)
    @Workflow.requires(state=has_footer)
    def process_footer(self):
        self.state['footer'] = self._process_text(self.state['footer'])

    @Workflow.method(priority=25)
    def finalize(self):
        height = self.options['height']

        header = self.state.get('header', '')
        body = self._join_text(self.state.get('body', []))
        footer = self._join_text(self.state.get('footer', []))

        header_nlines = header.count('\n')
        body_nlines = body.count('\n')
        footer_nlines = footer.count('\n')

        n_lines = (header_nlines + body_nlines + footer_nlines)
        if n_lines > height:
            raise ValueError("%s is to big, needs %d lines!" % (
                self.state['slide'], n_lines))

        body_footer_gap = height - n_lines - 1

        slide = [header]
        slide.append(body)
        slide.append("\n" * (body_footer_gap))
        slide.append(footer)

        self.state['full slide'] = ''.join(slide)

    @Workflow.requires(option='no_ascii_art', values=False)
    def _ascii_art_header(self):
        formatted = figlet_format(self.state['header'])
        self.state['header'] = formatted

    @Workflow.requires(option='no_ascii_art', values=True)
    def _basic_header(self):
        self.state['header'] = self.state['header'] + "\n\n"

    def _tokenize(self, text):
        """Terrible tokenizer

        Pygments supports restructured text, and is very likely to be a better
        and more full featured approach. Would avoid the need for this
        tokenizer
        """
        for line in text.splitlines():
            line = line.strip()

            if line.startswith("[code]"):
                code = line.split(']', 1)[-1]
                yield code, "code"
                continue

            for word in line.split():
                if attr_matchr.search(word):
                    attr = attr_matchr.search(word).group(2)
                    word = attr_matchr.search(word).group(4)
                elif word.startswith('*'):
                    attr = "bullet"
                else:
                    attr = None

                yield (word, attr)
            yield ("\n", None)

    def _apply_attribute(self, item, attribute):
        """Apply an attribute to a block of text"""
        if attribute not in attributes:
            raise ValueError("Unknown attribute: [%s](%s)" % (attribute, item))
        return attributes[attribute](item)

    def _process_text(self, text):
        """Take a chunk of text, examine and apply attributes as necessary"""
        if isinstance(text, list):
            text = '\n'.join(text)

        new_text = []
        for item, attribute in self._tokenize(text):
            new_text.append(self._apply_attribute(item, attribute))
        return new_text

    def _join_text(self, data):
        """Join the text as to avoid adding extra whitespace.

        This is embarassing.
        """
        to_join = []
        for v in data:
            to_join.append(v)
            if v[-1] != '\n':
                to_join.append(" ")
        return ''.join(to_join)
