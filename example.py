from pathfinder import find_paths

# get all directories and sub-directories in current directory
paths = find_paths(".", just_dirs=True)

# get all files in the current directory and all sub-directories
paths = find_paths(".", just_files=True)

# get all jpg files using a regex
paths = find_paths(".", regex=r".*\.jpg$")

# get all jpg files using posix wildcards
paths = find_paths(".", fnmatch="*.jpg")

# get all jpg files and png files
from pathfinder.filters import FnmatchFilter
from pathfinder.filters import OrFilter

jpg_filter = FnmatchFilter("*.jpg")
png_filter = FnmatchFilter("*.png")
gif_filter = FnmatchFilter("*.gif")
image_filter = OrFilter(jpg_filter, png_filter, gif_filter)
paths = find_paths(".", filter=image_filter)

# shortcut using bitwise or
paths = find_paths(".", filter=jpg_filter | png_filter | gif_filter)

# even shorter using ImageFilter to find all images
from pathfinder.filters import ImageFilter

paths = find_paths(".", filter=ImageFilter())

# and an even shorter way
paths = ImageFilter().find(".")
