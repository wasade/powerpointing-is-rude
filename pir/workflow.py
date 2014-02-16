#!/usr/bin/env python

import re
from bipy.core.workflow import Workflow
from pyfiglet import figlet_format
from functools import partial

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter

def color_wrapper(color, text):
    white = '\033[0m'
    return "%s%s%s" % (color, text, white)

pylex = PythonLexer()
term_format = TerminalFormatter()
def pygment_code(line):
    return highlight(line, pylex, term_format)

has_header = lambda x: 'header' in x
has_body = lambda x: 'body' in x
has_footer = lambda x: 'footer' in x

attr_matcher = re.compile("(?P<attr>\[([^]]+)\])(?P<text>\(([^]]+)\))")

ATTRIBUTES = {
        'red':partial(color_wrapper, '\033[91m'),
        'blue':partial(color_wrapper, '\033[94m'),
        'green':partial(color_wrapper, '\033[92m'),
        'bullet': lambda x: '    %s' % x,
        'code': pygment_code,
        None: lambda x: x}

def slide_iterator(data):
    if 'title' in data:
        title = data.pop('title')
        title['slide'] = 'title'
        yield title

    main_slides = [key for key in data if key.startswith('slide')]
    order = sorted(main_slides, key=lambda x: int(x.split()[-1]))

    for current_slide in order:
        slide = data[current_slide]
        slide['slide'] = current_slide
        yield slide

    if 'acknowledgements' in data:
        acks = data.pop('acknowledgements')
        acks['slide'] = 'acknowledgements'
        yield acks

class PowerPointingIsRude(Workflow):
    def initialize_state(self, item):
        self.state = item

    @Workflow.method(priority=100)
    @Workflow.requires(state=has_header)
    def process_header(self):
        formatted = figlet_format(self.state['header'])
        self.state['header'] = formatted

    @Workflow.method(priority=50)
    @Workflow.requires(state=has_body)
    def process_body(self):
        self.state['body'] = self._process_text(self.state['body'])

    @Workflow.method(priority=10)
    @Workflow.requires(state=has_footer)
    def process_footer(self):
        self.state['footer'] = self._process_text(self.state['footer'])

    @Workflow.method(priority=0)
    def finalize(self):
        header = self.state.get('header', '')
        body = self._join_text(self.state.get('body', []))
        footer = self._join_text(self.state.get('footer', []))

        header_nlines = header.count('\n')
        body_nlines = body.count('\n')
        footer_nlines = footer.count('\n')

        if header_nlines + body_nlines + footer_nlines > 25:
            raise ValueError("Slide %s is to big!" % self.state['slide'])

        body_footer_gap = 25 - (header_nlines + body_nlines) - footer_nlines

        slide = [header]
        slide.append(body)
        slide.append("\n" * (body_footer_gap))
        slide.append(footer)

        self.state['full slide'] = ''.join(slide)

    def _tokenize(self, text):
        for line in text.splitlines():
            line = line.strip()

            if line.startswith("[code]"):
                code = line.split(']', 1)[-1]
                yield code, "code"
                continue

            for word in line.split():
                if attr_matcher.search(word):
                    attr = attr_matcher.search(word).group(2)
                    word = attr_matcher.search(word).group(4)
                elif word.startswith('*'):
                    attr = "bullet"
                else:
                    attr = None

                yield (word, attr)
            yield ("\n", None)

    def _apply_attribute(self, item, attribute):
        if attribute not in ATTRIBUTES:
            raise ValueError("Unknown attribute: [%s](%s)" % (attribute, item))
        return ATTRIBUTES[attribute](item)

    def _process_text(self, text):
        if isinstance(text, list):
            text = '\n'.join(text)

        new_text = []
        for item, attribute in self._tokenize(text):
            new_text.append(self._apply_attribute(item, attribute))
        return new_text

    def _join_text(self, data):
        to_join = []
        for v in data:
            to_join.append(v)
            if v[-1] != '\n':
                to_join.append(" ")
        return ''.join(to_join)
