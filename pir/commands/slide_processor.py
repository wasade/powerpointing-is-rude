#!/usr/bin/env python
from __future__ import division

from types import GeneratorType
from pir.workflow import PowerpointingIsRude
from pir.iterators import slide_iterator
from pyqi.core.command import (Command, CommandIn, CommandOut,
    ParameterCollection)

class SlideProcessor(Command):
    BriefDescription = "Slide processor and formatter"
    LongDescription = "Process and validate slides, format, etc"
    CommandIns = ParameterCollection([
        CommandIn(Name='slides', DataType=dict,
                  Description='The input slides', Required=True),
        CommandIn(Name='height', DataType=int,
                  Description='The height of the window being used',
                  Required=False, Default=24), # need one for raw_input
        CommandIn(Name='width', DataType=int,
                  Description='The width of the window being used',
                  Required=False, Default=80),
        CommandIn(Name='no_ascii_art', DataType=bool,
                  Description='Disable ascii art', Default=False)
    ])

    CommandOuts = ParameterCollection([
        CommandOut(Name="formatted_slides", DataType=GeneratorType,
                   Description="Resulting formatted slides"),
    ])

    def run(self, **kwargs):
        success_f = lambda x: x.state['full slide']
        slides = kwargs.pop('slides')
        wf = PowerpointingIsRude({}, options=kwargs)
        iter_ = wf(slide_iterator(slides), success_callback=success_f)
        return {'formatted_slides':iter_}

CommandConstructor = SlideProcessor
