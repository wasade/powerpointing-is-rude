powerpointing is rude
=====================

A simple terminal based slide presenter because powerpoint is terrible.

Can I see some examples?
------------------------

Absolutely! The ``slide_processor`` is implemented as a [pyqi](http://pyqi.readthedocs.org) ``Command`` allowing for a nice clear CLI:

![Command Interface][0]

Sweet, nice and easy. But what do the slides look like? Awesome, of course:

![Color Example][1]

Yep. Pure awesome. And, the only direction to go from pure awesome is to über awesome (thank you [Pygments](http://pygments.org/)!):

![Code Example][2]

To install
----------

``pir`` currently depends on [bipy](https://github.com/biocore/bipy) which is unfortunately not ``pip`` installable directly at this time. The following should work though:

```bash
pip install numpy
pip install git+https://github.com/biocore/bipy.git
pip install pir
```

What now?
---------

To run the included slides, please execute:

```bash
pir slide-processor --slides=path/to/slides.json
```

Whats the format?
-----------------

The following JSON structure is expected for the slides:

```python
{
 "title": {"header": "foo", "body": ["line", ...], "footer": "bar"},
 "slide 1": {"header": "foo", "body": ["line", ...], "footer": "bar"},
 ...
 "acknowledgements": {"header": "foo", "body": ["line", ...], "footer": "bar"}
}
```

It is valid to omit ``header``, ``body`` or ``footer`` from a slide. ``body`` will accept single strings or list of strings. The order of the slides is based on the slide number. ``title`` and ``acknowledgements`` will go first and last respectively no matter what.

[0]: https://github.com/wasade/powerpointing-is-rude/raw/master/_assets/command.png
[1]: https://github.com/wasade/powerpointing-is-rude/raw/master/_assets/colors.png
[2]: https://github.com/wasade/powerpointing-is-rude/raw/master/_assets/code.png
