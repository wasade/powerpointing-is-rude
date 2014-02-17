#!/usr/bin/env python

from sys import exit

def slide_printer(result_key, data, option_value=None):
    for slide in data:
        print slide
        key = raw_input()

        if key == 'q':
            exit(0)
