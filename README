pathfinder
==========

A utility to find file paths.

Examples
--------

import pathfinder

# get all directories and sub-directories in current directory
paths = pathfinder.pathfind(".", just_dirs=True)

# get all directories and sub-directories in current directory
paths = pathfinder.pathfind(".", just_files=True)

# get all jpg files using a regex
paths = pathfinder.pathfind(".", regex=".*\.jpg$")

# get all jpg files using posix wildcards
paths = pathfinder.pathfind(".", fnmatch="*.jpg")

# get all jpg files and png files
jpg_filter = pathfinder.FnmatchFilter("*.jpg")
png_filter = pathfinder.FnmatchFilter("*.png")
image_filter = pathfinder.OrFilter(jpg_filter, png_filter)
paths = pathfinder.pathfind(".", filter=image_filter)
