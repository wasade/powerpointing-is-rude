#!/usr/bin/env python


def slide_iterator(data):
    """Yield the slides in order"""
    if 'title' in data:
        title = data.pop('title')
        title['slide'] = 'title'
        yield title

    main_slides = [key for key in data if key.startswith('slide')]
    order = sorted(main_slides, key=lambda x: float(x.split()[-1]))

    for current_slide in order:
        slide = data[current_slide]
        slide['slide'] = current_slide
        yield slide

    if 'acknowledgements' in data:
        acks = data.pop('acknowledgements')
        acks['slide'] = 'acknowledgements'
        yield acks
