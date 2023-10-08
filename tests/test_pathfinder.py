"""pathfinder tests module."""

import os

import pytest

from pathfinder import find_paths, walk_and_filter
from pathfinder.filters import (
    AndFilter,
    ColorImageFilter,
    DirectoryFilter,
    DotDirectoryFilter,
    FileFilter,
    FnmatchFilter,
    GreyscaleImageFilter,
    ImageDimensionFilter,
    ImageFilter,
    NotFilter,
    OrFilter,
    RegexFilter,
    SizeFilter,
)

BASEPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def test_just_dirs():
    """Test just_dirs parameter."""
    # only find directories
    paths = find_paths(BASEPATH, just_dirs=True)
    assert 5 == len(paths)
    assert os.path.join(BASEPATH, "dir1") in paths
    assert os.path.join(BASEPATH, "dir1", "subdirectory") in paths
    assert os.path.join(BASEPATH, "dir2") in paths
    assert os.path.join(BASEPATH, "dir3") in paths
    assert os.path.join(BASEPATH, ".dir4") in paths

    # use Filter.find
    paths_2 = DirectoryFilter().find(BASEPATH)
    assert paths == paths_2


def test_just_files():
    """Test just_files parameter."""
    # only find files
    paths = find_paths(BASEPATH, just_files=True)
    assert 18 == len(paths)
    assert os.path.join(BASEPATH, "file1.txt") in paths
    assert os.path.join(BASEPATH, "file2.dat") in paths
    assert os.path.join(BASEPATH, "file3.txt") in paths
    assert os.path.join(BASEPATH, "python_logo.gif") in paths
    assert os.path.join(BASEPATH, "python_logo.png") in paths
    assert os.path.join(BASEPATH, "python_logo_gs.gif") in paths
    assert os.path.join(BASEPATH, "python_logo_gs.jpg") in paths
    assert os.path.join(BASEPATH, "python_logo_gs.png") in paths
    assert os.path.join(BASEPATH, "transparent_gs.png") in paths
    assert os.path.join(BASEPATH, "dir1", "subdirectory", "sub.txt") in paths
    assert os.path.join(BASEPATH, "dir1", "file4.txt") in paths
    assert os.path.join(BASEPATH, "dir1", "file5.log") in paths
    assert os.path.join(BASEPATH, "dir2", "file6.log") in paths
    assert os.path.join(BASEPATH, "dir2", "file7.html") in paths
    assert os.path.join(BASEPATH, "dir3", "file8") in paths
    assert os.path.join(BASEPATH, "dir3", ".file9") in paths
    assert os.path.join(BASEPATH, ".dir4", "file10") in paths
    assert os.path.join(BASEPATH, ".dir4", "file20.txt") in paths

    # use Filter.find
    paths_2 = FileFilter().find(BASEPATH)
    assert paths == paths_2


def test_regex():
    """Test regex parameter."""
    # find all files and directories
    paths = find_paths(BASEPATH, regex=".*")
    assert 23 == len(paths)
    assert os.path.join(BASEPATH, "dir1") in paths
    assert os.path.join(BASEPATH, "dir1", "subdirectory") in paths
    assert os.path.join(BASEPATH, "dir2") in paths
    assert os.path.join(BASEPATH, "dir3") in paths
    assert os.path.join(BASEPATH, ".dir4") in paths
    assert os.path.join(BASEPATH, "file1.txt") in paths
    assert os.path.join(BASEPATH, "file2.dat") in paths
    assert os.path.join(BASEPATH, "file3.txt") in paths
    assert os.path.join(BASEPATH, "python_logo.gif") in paths
    assert os.path.join(BASEPATH, "python_logo.png") in paths
    assert os.path.join(BASEPATH, "python_logo_gs.gif") in paths
    assert os.path.join(BASEPATH, "python_logo_gs.jpg") in paths
    assert os.path.join(BASEPATH, "python_logo_gs.png") in paths
    assert os.path.join(BASEPATH, "transparent_gs.png") in paths
    assert os.path.join(BASEPATH, "dir1", "subdirectory", "sub.txt") in paths
    assert os.path.join(BASEPATH, "dir1", "file4.txt") in paths
    assert os.path.join(BASEPATH, "dir1", "file5.log") in paths
    assert os.path.join(BASEPATH, "dir2", "file6.log") in paths
    assert os.path.join(BASEPATH, "dir2", "file7.html") in paths
    assert os.path.join(BASEPATH, "dir3", "file8") in paths
    assert os.path.join(BASEPATH, "dir3", ".file9") in paths
    assert os.path.join(BASEPATH, ".dir4", "file10") in paths
    assert os.path.join(BASEPATH, ".dir4", "file20.txt") in paths

    # use Filter.find
    paths_2 = RegexFilter(".*").find(BASEPATH)
    assert paths == paths_2

    # find only files and directories with a t in the extension
    paths = find_paths(BASEPATH, regex=r".*\..*t.*$")
    assert 7 == len(paths)
    assert os.path.join(BASEPATH, "file1.txt") in paths
    assert os.path.join(BASEPATH, "file2.dat") in paths
    assert os.path.join(BASEPATH, "file3.txt") in paths
    assert os.path.join(BASEPATH, "dir1", "subdirectory", "sub.txt") in paths
    assert os.path.join(BASEPATH, "dir1", "file4.txt") in paths
    assert os.path.join(BASEPATH, "dir2", "file7.html") in paths
    assert os.path.join(BASEPATH, ".dir4", "file20.txt") in paths

    # find only files and directories with 1 anywhere in the path
    paths = find_paths(BASEPATH, regex=".*1.*")
    assert 7 == len(paths)
    assert os.path.join(BASEPATH, "dir1") in paths
    assert os.path.join(BASEPATH, "file1.txt") in paths
    assert os.path.join(BASEPATH, "dir1", "subdirectory") in paths
    assert os.path.join(BASEPATH, "dir1", "subdirectory", "sub.txt") in paths
    assert os.path.join(BASEPATH, "dir1", "file4.txt") in paths
    assert os.path.join(BASEPATH, "dir1", "file5.log") in paths
    assert os.path.join(BASEPATH, ".dir4", "file10") in paths


def test_fnmatch():
    """Test fnmatch parameter."""
    # find all files and directories
    paths = find_paths(BASEPATH, fnmatch="*")
    assert 23 == len(paths)
    assert os.path.join(BASEPATH, "dir1") in paths
    assert os.path.join(BASEPATH, "dir1", "subdirectory") in paths
    assert os.path.join(BASEPATH, "dir2") in paths
    assert os.path.join(BASEPATH, "dir3") in paths
    assert os.path.join(BASEPATH, ".dir4") in paths
    assert os.path.join(BASEPATH, "file1.txt") in paths
    assert os.path.join(BASEPATH, "file2.dat") in paths
    assert os.path.join(BASEPATH, "file3.txt") in paths
    assert os.path.join(BASEPATH, "python_logo.gif") in paths
    assert os.path.join(BASEPATH, "python_logo.png") in paths
    assert os.path.join(BASEPATH, "python_logo_gs.gif") in paths
    assert os.path.join(BASEPATH, "python_logo_gs.jpg") in paths
    assert os.path.join(BASEPATH, "python_logo_gs.png") in paths
    assert os.path.join(BASEPATH, "transparent_gs.png") in paths
    assert os.path.join(BASEPATH, "dir1", "subdirectory", "sub.txt") in paths
    assert os.path.join(BASEPATH, "dir1", "file4.txt") in paths
    assert os.path.join(BASEPATH, "dir1", "file5.log") in paths
    assert os.path.join(BASEPATH, "dir2", "file6.log") in paths
    assert os.path.join(BASEPATH, "dir2", "file7.html") in paths
    assert os.path.join(BASEPATH, "dir3", "file8") in paths
    assert os.path.join(BASEPATH, "dir3", ".file9") in paths
    assert os.path.join(BASEPATH, ".dir4", "file10") in paths
    assert os.path.join(BASEPATH, ".dir4", "file20.txt") in paths

    # find only files or directories with a .txt extension
    paths = find_paths(BASEPATH, fnmatch="*.txt")
    assert 5 == len(paths)
    assert os.path.join(BASEPATH, "file1.txt") in paths
    assert os.path.join(BASEPATH, "file3.txt") in paths
    assert os.path.join(BASEPATH, "dir1", "subdirectory", "sub.txt") in paths
    assert os.path.join(BASEPATH, "dir1", "file4.txt") in paths
    assert os.path.join(BASEPATH, ".dir4", "file20.txt") in paths


def test_all():
    """Test with no parameters."""
    # find all paths
    paths = find_paths(BASEPATH)
    assert 23 == len(paths)
    assert os.path.join(BASEPATH, "dir1") in paths
    assert os.path.join(BASEPATH, "dir1", "subdirectory") in paths
    assert os.path.join(BASEPATH, "dir2") in paths
    assert os.path.join(BASEPATH, "dir3") in paths
    assert os.path.join(BASEPATH, ".dir4") in paths
    assert os.path.join(BASEPATH, "file1.txt") in paths
    assert os.path.join(BASEPATH, "file2.dat") in paths
    assert os.path.join(BASEPATH, "file3.txt") in paths
    assert os.path.join(BASEPATH, "python_logo.gif") in paths
    assert os.path.join(BASEPATH, "python_logo.png") in paths
    assert os.path.join(BASEPATH, "python_logo_gs.gif") in paths
    assert os.path.join(BASEPATH, "python_logo_gs.jpg") in paths
    assert os.path.join(BASEPATH, "python_logo_gs.png") in paths
    assert os.path.join(BASEPATH, "transparent_gs.png") in paths
    assert os.path.join(BASEPATH, "dir1", "subdirectory", "sub.txt") in paths
    assert os.path.join(BASEPATH, "dir1", "file4.txt") in paths
    assert os.path.join(BASEPATH, "dir1", "file5.log") in paths
    assert os.path.join(BASEPATH, "dir2", "file6.log") in paths
    assert os.path.join(BASEPATH, "dir2", "file7.html") in paths
    assert os.path.join(BASEPATH, "dir3", "file8") in paths
    assert os.path.join(BASEPATH, "dir3", ".file9") in paths
    assert os.path.join(BASEPATH, ".dir4", "file10") in paths
    assert os.path.join(BASEPATH, ".dir4", "file20.txt") in paths


def test_and():
    """Test AndFilter."""
    # find directories with a 2 anywhere in the path
    filt = AndFilter(DirectoryFilter(), RegexFilter(".*2.*"))
    paths = find_paths(BASEPATH, filter=filt)
    assert 1 == len(paths)
    assert os.path.join(BASEPATH, "dir2") in paths

    # test overridden __and__
    filt = DirectoryFilter() & RegexFilter(".*2.*")
    paths_2 = find_paths(BASEPATH, filter=filt)
    assert paths == paths_2

    # use Filter.find
    paths_3 = AndFilter(DirectoryFilter(), RegexFilter(".*2.*")).find(BASEPATH)
    assert paths == paths_3


def test_or():
    """Test OrFilter."""
    # find all directories and any files (or directories)
    # with 2 in the path
    filt = OrFilter(DirectoryFilter(), RegexFilter(".*2.*"))
    paths = find_paths(BASEPATH, filter=filt)
    assert 9 == len(paths)
    assert os.path.join(BASEPATH, "dir1") in paths
    assert os.path.join(BASEPATH, "dir1", "subdirectory") in paths
    assert os.path.join(BASEPATH, "dir2") in paths
    assert os.path.join(BASEPATH, "dir3") in paths
    assert os.path.join(BASEPATH, ".dir4") in paths
    assert os.path.join(BASEPATH, ".dir4", "file20.txt") in paths
    assert os.path.join(BASEPATH, "file2.dat") in paths
    assert os.path.join(BASEPATH, "dir2", "file6.log") in paths
    assert os.path.join(BASEPATH, "dir2", "file7.html") in paths

    # test overridden __or__
    filt = DirectoryFilter() | RegexFilter(".*2.*")
    paths_2 = find_paths(BASEPATH, filter=filt)
    assert paths == paths_2

    # use Filter.find
    paths_3 = OrFilter(DirectoryFilter(), RegexFilter(".*2.*")).find(BASEPATH)
    assert paths == paths_3


def test_not():
    """Test NotFilter."""
    # find all files and directories with a .txt extension
    # except ones that end in 3.txt
    filt = AndFilter(NotFilter(FnmatchFilter("*3.txt")), FnmatchFilter("*.txt"))
    paths = find_paths(BASEPATH, filter=filt)
    assert 4 == len(paths)
    assert os.path.join(BASEPATH, "file1.txt") in paths
    assert os.path.join(BASEPATH, "dir1", "subdirectory", "sub.txt") in paths
    assert os.path.join(BASEPATH, "dir1", "file4.txt") in paths
    assert os.path.join(BASEPATH, ".dir4", "file20.txt") in paths


def test_ignore():
    """Test ignore parameter."""
    # find all directories and all files and directories
    # with a 2 in the path and no directories that begin
    # with a dot
    filt = OrFilter(DirectoryFilter(), RegexFilter(".*2.*"))
    ignore = DotDirectoryFilter()
    paths = find_paths(BASEPATH, filter=filt, ignore=ignore)
    assert 7 == len(paths)
    assert os.path.join(BASEPATH, "dir1") in paths
    assert os.path.join(BASEPATH, "dir1", "subdirectory") in paths
    assert os.path.join(BASEPATH, "dir2") in paths
    assert os.path.join(BASEPATH, "dir3") in paths
    assert os.path.join(BASEPATH, "file2.dat") in paths
    assert os.path.join(BASEPATH, "dir2", "file6.log") in paths
    assert os.path.join(BASEPATH, "dir2", "file7.html") in paths
    # verify the files n the .dir4 directory is not found
    assert os.path.join(BASEPATH, ".dir4", "file10") not in paths
    assert os.path.join(BASEPATH, ".dir4", "file20.txt") not in paths

    filt = FnmatchFilter("*.txt")
    ignore = FnmatchFilter("*4.txt")

    all_paths = find_paths(BASEPATH, filter=filt)
    assert 5 == len(all_paths)
    assert "4.txt" in " ".join(all_paths)

    ignore_paths = find_paths(BASEPATH, filter=filt, ignore=ignore)
    assert 4 == len(ignore_paths)
    assert "4.txt" not in " ".join(ignore_paths)


def test_abspath():
    """Make sure all paths are absolute paths."""
    cwd = os.getcwd()
    paths = find_paths(BASEPATH, filter=DirectoryFilter(), abspath=True)
    assert 5 == len(paths)
    assert os.path.join(cwd, BASEPATH, "dir1") in paths
    assert os.path.join(cwd, BASEPATH, "dir1", "subdirectory") in paths
    assert os.path.join(cwd, BASEPATH, "dir2") in paths
    assert os.path.join(cwd, BASEPATH, "dir3") in paths
    assert os.path.join(cwd, BASEPATH, ".dir4") in paths

    paths = find_paths(BASEPATH, just_files=True, abspath=True)
    assert 18 == len(paths)
    assert os.path.join(cwd, BASEPATH, "python_logo.png") in paths


def test_depth():
    """Only descend a certain depth into a tree."""
    paths = find_paths(BASEPATH, filter=DirectoryFilter(), depth=1)
    assert 4 == len(paths)
    assert os.path.join(BASEPATH, "dir1") in paths
    assert os.path.join(BASEPATH, "dir2") in paths
    assert os.path.join(BASEPATH, "dir3") in paths
    assert os.path.join(BASEPATH, ".dir4") in paths

    paths = find_paths(BASEPATH, filter=DirectoryFilter(), depth=2)
    assert 5 == len(paths)
    assert os.path.join(BASEPATH, "dir1", "subdirectory") in paths


def test_size():
    """Find files based on size criteria."""
    # all files except the image files are less than 10 bytes
    p_filter = SizeFilter(max_bytes=0)
    paths = walk_and_filter(BASEPATH, p_filter)
    assert 12 == len(paths)

    # only the image files contain data
    p_filter = SizeFilter(min_bytes=1)
    paths = walk_and_filter(BASEPATH, p_filter)
    assert 6 == len(paths)

    # three images between 450 bytes and 9000
    p_filter = SizeFilter(min_bytes=450, max_bytes=9000)
    paths = walk_and_filter(BASEPATH, p_filter)
    assert 3 == len(paths)


def test_image():
    """Find all images."""
    image_filter = ImageFilter()
    paths = walk_and_filter(BASEPATH, image_filter)
    assert 6 == len(paths)


def test_find_filepath():
    """Test when the root path to a find is a file and not a directory."""
    a_paths = find_paths(os.path.join(BASEPATH, "python_logo.png"), just_files=True)
    b_paths = find_paths(BASEPATH, just_files=True)
    assert a_paths == b_paths


try:
    import PIL  # noqa: F401

    def test_image_dimension():
        """Find images based on dimensions."""
        p_filter = ImageDimensionFilter(
            max_width=1000, max_height=1000, min_height=20, min_width=20
        )
        paths = walk_and_filter(BASEPATH, p_filter)
        assert 6 == len(paths)

        # ignore the 24x24
        p_filter = ImageDimensionFilter(
            max_width=1000, max_height=1000, min_height=25, min_width=25
        )
        paths = walk_and_filter(BASEPATH, p_filter)
        assert 5 == len(paths)

        # no 24x24, but only check it based on height
        p_filter = ImageDimensionFilter(min_height=25)
        paths = walk_and_filter(BASEPATH, p_filter)
        assert 5 == len(paths)

        # only the 24x24
        p_filter = ImageDimensionFilter(max_width=24, max_height=24)
        paths = walk_and_filter(BASEPATH, p_filter)
        assert 1 == len(paths)

        # only the 24x24, but only check it based on height
        p_filter = ImageDimensionFilter(max_height=24)
        paths = walk_and_filter(BASEPATH, p_filter)
        assert 1 == len(paths)

        # no parameters - all images
        p_filter = ImageDimensionFilter()
        paths = walk_and_filter(BASEPATH, p_filter)
        assert 6 == len(paths)

    def test_bw_image():
        """Find all grey scale images."""
        p_filter = GreyscaleImageFilter()
        paths = walk_and_filter(BASEPATH, p_filter)
        assert 4 == len(paths)

    def test_color_image():
        """Find all color images."""
        p_filter = ColorImageFilter()
        paths = walk_and_filter(BASEPATH, p_filter)
        assert 2 == len(paths)

except ImportError:
    pass


def test_generator():
    """Test with no parameters."""
    # find all paths
    paths = []
    for path in find_paths(BASEPATH):
        paths.append(path)
    assert 23 == len(paths)
    assert os.path.join(BASEPATH, "dir1") in paths
    assert os.path.join(BASEPATH, "dir1", "subdirectory") in paths
    assert os.path.join(BASEPATH, "dir2") in paths
    assert os.path.join(BASEPATH, "dir3") in paths
    assert os.path.join(BASEPATH, ".dir4") in paths
    assert os.path.join(BASEPATH, "file1.txt") in paths
    assert os.path.join(BASEPATH, "file2.dat") in paths
    assert os.path.join(BASEPATH, "file3.txt") in paths
    assert os.path.join(BASEPATH, "python_logo.gif") in paths
    assert os.path.join(BASEPATH, "python_logo.png") in paths
    assert os.path.join(BASEPATH, "python_logo_gs.gif") in paths
    assert os.path.join(BASEPATH, "python_logo_gs.jpg") in paths
    assert os.path.join(BASEPATH, "python_logo_gs.png") in paths
    assert os.path.join(BASEPATH, "transparent_gs.png") in paths
    assert os.path.join(BASEPATH, "dir1", "subdirectory", "sub.txt") in paths
    assert os.path.join(BASEPATH, "dir1", "file4.txt") in paths
    assert os.path.join(BASEPATH, "dir1", "file5.log") in paths
    assert os.path.join(BASEPATH, "dir2", "file6.log") in paths
    assert os.path.join(BASEPATH, "dir2", "file7.html") in paths
    assert os.path.join(BASEPATH, "dir3", "file8") in paths
    assert os.path.join(BASEPATH, "dir3", ".file9") in paths
    assert os.path.join(BASEPATH, ".dir4", "file10") in paths
    assert os.path.join(BASEPATH, ".dir4", "file20.txt") in paths


def test_path_does_not_exist():
    """Test when the parameter is a non-existent path."""
    # only find directories
    with pytest.raises(EnvironmentError):
        find_paths(
            os.path.join(os.path.dirname(BASEPATH), "doesnotexist"), just_dirs=True
        )
