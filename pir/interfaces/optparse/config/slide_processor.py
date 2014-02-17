#!/usr/bin/env python
from __future__ import division

__credits__ = []

from pyqi.core.interfaces.optparse import (OptparseUsageExample,
                                           OptparseOption, OptparseResult)
from pyqi.core.command import (make_command_in_collection_lookup_f,
                               make_command_out_collection_lookup_f)
from pir.commands.slide_processor import CommandConstructor
from pir.interfaces.optparse.input_handler import json_loader
from pir.interfaces.optparse.output_handler import slide_printer

# Convenience function for looking up parameters by name.
cmd_in_lookup = make_command_in_collection_lookup_f(CommandConstructor)
cmd_out_lookup = make_command_out_collection_lookup_f(CommandConstructor)

# Examples of how the command can be used from the command line using an
# optparse interface.
usage_examples = [
    OptparseUsageExample(ShortDesc="Present some slides",
                         LongDesc="Present all of the slides!!",
                         Ex="%prog --slides=some_file")
]

inputs = [
    OptparseOption(Parameter=cmd_in_lookup('height'),
                   Type=int,
                   Action='store', # default is 'store', change if desired
                   Handler=None, # must be defined if desired
                   ShortName=None, # must be defined if desired
                   ),
    OptparseOption(Parameter=cmd_in_lookup('slides'),
                   Type=str,
                   Action='store', # default is 'store', change if desired
                   Handler=json_loader, # must be defined if desired
                   ShortName=None, # must be defined if desired
                   ),
    OptparseOption(Parameter=cmd_in_lookup('width'),
                   Type=int,
                   Action='store', # default is 'store', change if desired
                   Handler=None, # must be defined if desired
                   ShortName=None, # must be defined if desired
                   ),
    OptparseOption(Parameter=cmd_in_lookup('no_ascii_art'),
                   Type=None,
                   Action='store_true'
                   )
]

outputs = [
    OptparseResult(Parameter=cmd_out_lookup('formatted_slides'),
                    Handler=slide_printer, # must be defined
                    InputName=None), # define if tying to an OptparseOption
]
