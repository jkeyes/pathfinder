.. pathfinder documentation master file, created by
   sphinx-quickstart on Mon Apr 23 22:46:06 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. toctree::
   :hidden:

   api

==========
pathfinder
==========

pathfinder is `os.walk` for humans.

Installation
============

Stable releases of pathfinder can be installed with 
`pip <http://pip.openplans.org>`_ or you may download a `.tgz` source 
archive from `pypi <http://pypi.python.org/pypi/pathfinder#downloads>`_.
See the :doc:`installation` page for more detailed instructions.

If you want to use the latest code, you can grab it from our 
`Git repository <http://github.com/jkeyes/pathfinder>`_, or `fork it <http://github.com/jkeyes/pathfinder>`_.

Usage
=====

Basic find
----------

::

    from pathfinder import find

    # all files and directories
    paths = find(".")

    # all files
    paths = find(".", just_files=True)

    # all directories
    paths = find(".", just_dirs=True)

By default `find` prepends the path you search for to the results.
If you want you can ensure the results only contain absolute paths:

::

    paths = find(".", abspath=True)

Filtering the results
---------------------

Having a full listing is useful but wouldn't it be great if we could
filter the results.

There a are a number of ways we can do this. Let's start with 
the `Unix shell-style pattern <http://docs.python.org/library/fnmatch.html>`_ approach:

::

    # all PDF files
    paths = find(".", fnmatch="*.pdf")

fnmatching provides some power, but for more flexibility lets
have a look at the regular expression support:

::

    # all PDF files
    paths = find(".", regex=".*\.pdf")

    # all PDF files with four letter base names
    paths = find(pwd, regex=".*/.{4}\.pdf")

pathfinder provides the ability to ignore certain paths too:

::

    # create your ignore filter to ignore all PDF files
    # from the files with three character extensions
    from pathfinder import FnmatchFilter
    ignore = FnmatchFilter("*.pdf")
    find(".", regex=".*/.*\..{3}$", ignore=ignore)

    # ignore all files and directories that begin with .
    ignore = RegexFilter("\..*")    
    find(".", ignore=ignore)

Controlling the depth of the search
-----------------------------------

You may want to limit how to deep to search into a directory tree:

::

    # only search down two levels
    find(".", depth=2)

Extra support for images
------------------------

Let's find some images in the directory:

::

    # all of the images
    from pathfinder import ImageFilter
    find(".", filter=ImageFilter())

That is just a shortcut for matching multiple file extensions, 
but we can also filter the results based on the dimensions of the 
image:

::

    # only images less than 20 pixels tall
    from pathfinder import ImageDimensionFilter
    find(".", filter=ImageDimensionFilter(max_height=20))

    # only images less than 10 pixels tall and wide
    from pathfinder import ImageDimensionFilter
    find(".", filter=ImageDimensionFilter(max_height=10, min_height=10))

And we can also search for images based on their color paletter:

::

    # only color images
    from pathfinder import ColorImageFilter
    find(".", filter=ColorImageFilter())

    # only greyscale images
    from pathfinder import GreyscaleImageFilter
    find(".", filter=GreyscaleImageFilter())

