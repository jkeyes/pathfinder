pathfinder
==========

A utility to find file paths.

.. image:: https://snyk.io/test/github/jkeyes/pathfinder/badge.svg
    :target: https://snyk.io/test/github/jkeyes/pathfinder

|

.. image:: https://travis-ci.org/jkeyes/pathfinder.png?branch=master
    :target: https://travis-ci.org/jkeyes/pathfinder

|

.. image:: https://static.deepsource.io/deepsource-badge-light.svg
    :target: https://deepsource.io/gh/jkeyes/pathfinder/?ref=repository-badge


Examples
--------

.. code-block:: python

    from pathfinder import find_paths

    # get all directories and sub-directories in current directory
    paths = find_paths(".", just_dirs=True)

    # get all files in the current directory and all sub-directories
    paths = find_paths(".", just_files=True)

    # get all jpg files using a regex
    paths = find_paths(".", regex=".*\.jpg$")

    # get all jpg files using posix wildcards
    paths = find_paths(".", fnmatch="*.jpg")

    # get all jpg files and png files
    from pathfinder import FnmatchFilter
    from pathfinder import OrFilter
    jpg_filter = FnmatchFilter("*.jpg")
    png_filter = FnmatchFilter("*.png")
    gif_filter = FnmatchFilter("*.gif")
    image_filter = OrFilter(jpg_filter, png_filter, gif_filter)
    paths = find_paths(".", filter=image_filter)

    # shortcut using bitwise or
    paths = find_paths(".", filter=jpg_filter | png_filter | gif_filter)

    # even shorter using ImageFilter to find all images
    from pathfinder import ImageFilter
    paths = find_paths(".", filter=ImageFilter())

    # and an even shorter way
    paths = ImageFilter().find(".")


Installation
------------

To install pathfinder, simply:

.. code-block:: bash

    $ pip install pathfinder

Development
-----------

To install development dependencies run:

.. code-block:: bash

    $ pip install -r dev-requirements.txt
