#!/usr/bin/env python

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

attributes = {
    'red': partial(color_wrapper, '\033[91m'),
    'blue': partial(color_wrapper, '\033[94m'),
    'green': partial(color_wrapper, '\033[92m'),
    'bullet': lambda x: '    %s' % x,
    'code': pygment_code,
    None: lambda x: x}
