Changelog
=========

0.6.1
+++++
* fixed example in README.rst

0.6.0
+++++
* removed deprecated find and pathfind functions

0.5.4
+++++
* resolving security alert regarding the version of jinja2

0.5.3
+++++
* do not `chdir` in `walk_and_filter_generator`. `#3 <https://github.com/jkeyes/pathfinder/pull/3>`_. (https://github.com/rubik)

0.5.2
+++++
* Silly error in MANIFEST.in resolved.

0.5.1
+++++
* Added README.rst to MANIFEST.in to prevent install error from pip.

0.5
+++
* new find_paths function returns a generator
* using any and all in OrFiter and AndFilter

0.4.1
+++++
* Fixed install error in setup.py

0.4
+++
* File size filter
* Image filter
* Image dimensions filter
* Color image filter
* Greyscale image filter
* moved code to pathfinder package
* use nose for testing
* changed license from BSD to MIT
* override __or__ and __and__ for easy compound filter creation
* new Filter.find method
* ignore now works for filepaths

0.3.1
+++++
* Removed hard-coded file separators
* Added docstrings and comments

0.3
+++
* Added depth parameter to walk_and_filter

0.2
+++
* Added setup.py
* Fixed bug in NotFilter
* Tided pathfind function.

0.1
+++
* First Cut
