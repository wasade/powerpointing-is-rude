powerpointing is rude
=====================

A simple terminal based slide presenter because powerpoint is terrible.

To install
----------

``pir`` currently depends on [bipy](https://github.com/biocore/bipy) which is unfortunately not ``pip`` installable at this time. Please see the ``bipy`` project for installation instructions. Once ``bipy`` is installed, please simply run:

```bash
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

