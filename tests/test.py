"""pathfinder tests module."""

import os
import unittest

from pathfinder import find_paths
from pathfinder import walk_and_filter
from pathfinder.filters import (
    SizeFilter,
    DirectoryFilter,
    FileFilter,
    RegexFilter,
    AndFilter,
    OrFilter,
    NotFilter,
    FnmatchFilter,
    DotDirectoryFilter,
    ImageDimensionFilter,
    ImageFilter,
    ColorImageFilter,
    GreyscaleImageFilter,
)

BASEPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


class FindTest(unittest.TestCase):
    """Test case."""

    def test_just_dirs(self):
        """Test just_dirs parameter."""
        # only find directories
        paths = find_paths(BASEPATH, just_dirs=True)
        self.assertEqual(5, len(paths))
        self.assertTrue(os.path.join(BASEPATH, "dir1") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir1", "subdirectory") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir2") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir3") in paths)
        self.assertTrue(os.path.join(BASEPATH, ".dir4") in paths)

        # use Filter.find
        paths_2 = DirectoryFilter().find(BASEPATH)
        self.assertEqual(paths, paths_2)

    def test_just_files(self):
        """Test just_files parameter."""
        # only find files
        paths = find_paths(BASEPATH, just_files=True)
        self.assertEqual(18, len(paths))
        self.assertTrue(os.path.join(BASEPATH, "file1.txt") in paths)
        self.assertTrue(os.path.join(BASEPATH, "file2.dat") in paths)
        self.assertTrue(os.path.join(BASEPATH, "file3.txt") in paths)
        self.assertTrue(os.path.join(BASEPATH, "python_logo.gif") in paths)
        self.assertTrue(os.path.join(BASEPATH, "python_logo.png") in paths)
        self.assertTrue(os.path.join(BASEPATH, "python_logo_gs.gif") in paths)
        self.assertTrue(os.path.join(BASEPATH, "python_logo_gs.jpg") in paths)
        self.assertTrue(os.path.join(BASEPATH, "python_logo_gs.png") in paths)
        self.assertTrue(os.path.join(BASEPATH, "transparent_gs.png") in paths)
        self.assertTrue(
            os.path.join(BASEPATH, "dir1", "subdirectory", "sub.txt") in paths
        )
        self.assertTrue(os.path.join(BASEPATH, "dir1", "file4.txt") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir1", "file5.log") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir2", "file6.log") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir2", "file7.html") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir3", "file8") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir3", ".file9") in paths)
        self.assertTrue(os.path.join(BASEPATH, ".dir4", "file10") in paths)
        self.assertTrue(os.path.join(BASEPATH, ".dir4", "file20.txt") in paths)

        # use Filter.find
        paths_2 = FileFilter().find(BASEPATH)
        self.assertEqual(paths, paths_2)

    def test_regex(self):
        """Test regex parameter."""
        # find all files and directories
        paths = find_paths(BASEPATH, regex=".*")
        self.assertEqual(23, len(paths))
        self.assertTrue(os.path.join(BASEPATH, "dir1") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir1", "subdirectory") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir2") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir3") in paths)
        self.assertTrue(os.path.join(BASEPATH, ".dir4") in paths)
        self.assertTrue(os.path.join(BASEPATH, "file1.txt") in paths)
        self.assertTrue(os.path.join(BASEPATH, "file2.dat") in paths)
        self.assertTrue(os.path.join(BASEPATH, "file3.txt") in paths)
        self.assertTrue(os.path.join(BASEPATH, "python_logo.gif") in paths)
        self.assertTrue(os.path.join(BASEPATH, "python_logo.png") in paths)
        self.assertTrue(os.path.join(BASEPATH, "python_logo_gs.gif") in paths)
        self.assertTrue(os.path.join(BASEPATH, "python_logo_gs.jpg") in paths)
        self.assertTrue(os.path.join(BASEPATH, "python_logo_gs.png") in paths)
        self.assertTrue(os.path.join(BASEPATH, "transparent_gs.png") in paths)
        self.assertTrue(
            os.path.join(BASEPATH, "dir1", "subdirectory", "sub.txt") in paths
        )
        self.assertTrue(os.path.join(BASEPATH, "dir1", "file4.txt") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir1", "file5.log") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir2", "file6.log") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir2", "file7.html") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir3", "file8") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir3", ".file9") in paths)
        self.assertTrue(os.path.join(BASEPATH, ".dir4", "file10") in paths)
        self.assertTrue(os.path.join(BASEPATH, ".dir4", "file20.txt") in paths)

        # use Filter.find
        paths_2 = RegexFilter(".*").find(BASEPATH)
        self.assertEqual(paths, paths_2)

        # find only files and directories with a t in the extension
        paths = find_paths(BASEPATH, regex=r".*\..*t.*$")
        self.assertEqual(7, len(paths))
        self.assertTrue(os.path.join(BASEPATH, "file1.txt") in paths)
        self.assertTrue(os.path.join(BASEPATH, "file2.dat") in paths)
        self.assertTrue(os.path.join(BASEPATH, "file3.txt") in paths)
        self.assertTrue(
            os.path.join(BASEPATH, "dir1", "subdirectory", "sub.txt") in paths
        )
        self.assertTrue(os.path.join(BASEPATH, "dir1", "file4.txt") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir2", "file7.html") in paths)
        self.assertTrue(os.path.join(BASEPATH, ".dir4", "file20.txt") in paths)

        # find only files and directories with 1 anywhere in the path
        paths = find_paths(BASEPATH, regex=".*1.*")
        self.assertEqual(7, len(paths))
        self.assertTrue(os.path.join(BASEPATH, "dir1") in paths)
        self.assertTrue(os.path.join(BASEPATH, "file1.txt") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir1", "subdirectory") in paths)
        self.assertTrue(
            os.path.join(BASEPATH, "dir1", "subdirectory", "sub.txt") in paths
        )
        self.assertTrue(os.path.join(BASEPATH, "dir1", "file4.txt") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir1", "file5.log") in paths)
        self.assertTrue(os.path.join(BASEPATH, ".dir4", "file10") in paths)

    def test_fnmatch(self):
        """Test fnmatch parameter."""
        # find all files and directories
        paths = find_paths(BASEPATH, fnmatch="*")
        self.assertEqual(23, len(paths))
        self.assertTrue(os.path.join(BASEPATH, "dir1") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir1", "subdirectory") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir2") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir3") in paths)
        self.assertTrue(os.path.join(BASEPATH, ".dir4") in paths)
        self.assertTrue(os.path.join(BASEPATH, "file1.txt") in paths)
        self.assertTrue(os.path.join(BASEPATH, "file2.dat") in paths)
        self.assertTrue(os.path.join(BASEPATH, "file3.txt") in paths)
        self.assertTrue(os.path.join(BASEPATH, "python_logo.gif") in paths)
        self.assertTrue(os.path.join(BASEPATH, "python_logo.png") in paths)
        self.assertTrue(os.path.join(BASEPATH, "python_logo_gs.gif") in paths)
        self.assertTrue(os.path.join(BASEPATH, "python_logo_gs.jpg") in paths)
        self.assertTrue(os.path.join(BASEPATH, "python_logo_gs.png") in paths)
        self.assertTrue(os.path.join(BASEPATH, "transparent_gs.png") in paths)
        self.assertTrue(
            os.path.join(BASEPATH, "dir1", "subdirectory", "sub.txt") in paths
        )
        self.assertTrue(os.path.join(BASEPATH, "dir1", "file4.txt") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir1", "file5.log") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir2", "file6.log") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir2", "file7.html") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir3", "file8") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir3", ".file9") in paths)
        self.assertTrue(os.path.join(BASEPATH, ".dir4", "file10") in paths)
        self.assertTrue(os.path.join(BASEPATH, ".dir4", "file20.txt") in paths)

        # find only files or directories with a .txt extension
        paths = find_paths(BASEPATH, fnmatch="*.txt")
        self.assertEqual(5, len(paths))
        self.assertTrue(os.path.join(BASEPATH, "file1.txt") in paths)
        self.assertTrue(os.path.join(BASEPATH, "file3.txt") in paths)
        self.assertTrue(
            os.path.join(BASEPATH, "dir1", "subdirectory", "sub.txt") in paths
        )
        self.assertTrue(os.path.join(BASEPATH, "dir1", "file4.txt") in paths)
        self.assertTrue(os.path.join(BASEPATH, ".dir4", "file20.txt") in paths)

    def test_all(self):
        """Test with no parameters."""
        # find all paths
        paths = find_paths(BASEPATH)
        self.assertEqual(23, len(paths))
        self.assertTrue(os.path.join(BASEPATH, "dir1") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir1", "subdirectory") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir2") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir3") in paths)
        self.assertTrue(os.path.join(BASEPATH, ".dir4") in paths)
        self.assertTrue(os.path.join(BASEPATH, "file1.txt") in paths)
        self.assertTrue(os.path.join(BASEPATH, "file2.dat") in paths)
        self.assertTrue(os.path.join(BASEPATH, "file3.txt") in paths)
        self.assertTrue(os.path.join(BASEPATH, "python_logo.gif") in paths)
        self.assertTrue(os.path.join(BASEPATH, "python_logo.png") in paths)
        self.assertTrue(os.path.join(BASEPATH, "python_logo_gs.gif") in paths)
        self.assertTrue(os.path.join(BASEPATH, "python_logo_gs.jpg") in paths)
        self.assertTrue(os.path.join(BASEPATH, "python_logo_gs.png") in paths)
        self.assertTrue(os.path.join(BASEPATH, "transparent_gs.png") in paths)
        self.assertTrue(
            os.path.join(BASEPATH, "dir1", "subdirectory", "sub.txt") in paths
        )
        self.assertTrue(os.path.join(BASEPATH, "dir1", "file4.txt") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir1", "file5.log") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir2", "file6.log") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir2", "file7.html") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir3", "file8") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir3", ".file9") in paths)
        self.assertTrue(os.path.join(BASEPATH, ".dir4", "file10") in paths)
        self.assertTrue(os.path.join(BASEPATH, ".dir4", "file20.txt") in paths)

    def test_and(self):
        """Test AndFilter."""
        # find directories with a 2 anywhere in the path
        filt = AndFilter(DirectoryFilter(), RegexFilter(".*2.*"))
        paths = find_paths(BASEPATH, filter=filt)
        self.assertEqual(1, len(paths))
        self.assertTrue(os.path.join(BASEPATH, "dir2") in paths)

        # test overridden __and__
        filt = DirectoryFilter() & RegexFilter(".*2.*")
        paths_2 = find_paths(BASEPATH, filter=filt)
        self.assertEqual(paths, paths_2)

        # use Filter.find
        paths_3 = AndFilter(DirectoryFilter(), RegexFilter(".*2.*")).find(BASEPATH)
        self.assertEqual(paths, paths_3)

    def test_or(self):
        """Test OrFilter."""
        # find all directories and any files (or directories)
        # with 2 in the path
        filt = OrFilter(DirectoryFilter(), RegexFilter(".*2.*"))
        paths = find_paths(BASEPATH, filter=filt)
        self.assertEqual(9, len(paths))
        self.assertTrue(os.path.join(BASEPATH, "dir1") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir1", "subdirectory") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir2") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir3") in paths)
        self.assertTrue(os.path.join(BASEPATH, ".dir4") in paths)
        self.assertTrue(os.path.join(BASEPATH, ".dir4", "file20.txt") in paths)
        self.assertTrue(os.path.join(BASEPATH, "file2.dat") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir2", "file6.log") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir2", "file7.html") in paths)

        # test overridden __or__
        filt = DirectoryFilter() | RegexFilter(".*2.*")
        paths_2 = find_paths(BASEPATH, filter=filt)
        self.assertEqual(paths, paths_2)

        # use Filter.find
        paths_3 = OrFilter(DirectoryFilter(), RegexFilter(".*2.*")).find(BASEPATH)
        self.assertEqual(paths, paths_3)

    def test_not(self):
        """Test NotFilter."""
        # find all files and directories with a .txt extension
        # except ones that end in 3.txt
        filt = AndFilter(NotFilter(FnmatchFilter("*3.txt")), FnmatchFilter("*.txt"))
        paths = find_paths(BASEPATH, filter=filt)
        self.assertEqual(4, len(paths))
        self.assertTrue(os.path.join(BASEPATH, "file1.txt") in paths)
        self.assertTrue(
            os.path.join(BASEPATH, "dir1", "subdirectory", "sub.txt") in paths
        )
        self.assertTrue(os.path.join(BASEPATH, "dir1", "file4.txt") in paths)
        self.assertTrue(os.path.join(BASEPATH, ".dir4", "file20.txt") in paths)

    def test_ignore(self):
        """Test ignore parameter."""
        # find all directories and all files and directories
        # with a 2 in the path and no directories that begin
        # with a dot
        filt = OrFilter(DirectoryFilter(), RegexFilter(".*2.*"))
        ignore = DotDirectoryFilter()
        paths = find_paths(BASEPATH, filter=filt, ignore=ignore)
        self.assertEqual(7, len(paths))
        self.assertTrue(os.path.join(BASEPATH, "dir1") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir1", "subdirectory") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir2") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir3") in paths)
        self.assertTrue(os.path.join(BASEPATH, "file2.dat") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir2", "file6.log") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir2", "file7.html") in paths)
        # verify the files n the .dir4 directory is not found
        self.assertTrue(os.path.join(BASEPATH, ".dir4", "file10") not in paths)
        self.assertTrue(os.path.join(BASEPATH, ".dir4", "file20.txt") not in paths)

        filt = FnmatchFilter("*.txt")
        ignore = FnmatchFilter("*4.txt")

        all_paths = find_paths(BASEPATH, filter=filt)
        self.assertEqual(5, len(all_paths))
        self.assertTrue("4.txt" in " ".join(all_paths))

        ignore_paths = find_paths(BASEPATH, filter=filt, ignore=ignore)
        self.assertEqual(4, len(ignore_paths))
        self.assertFalse("4.txt" in " ".join(ignore_paths))

    def test_abspath(self):
        """Make sure all paths are absolute paths."""
        cwd = os.getcwd()
        paths = find_paths(BASEPATH, filter=DirectoryFilter(), abspath=True)
        self.assertEqual(5, len(paths))
        self.assertTrue(os.path.join(cwd, BASEPATH, "dir1") in paths)
        self.assertTrue(os.path.join(cwd, BASEPATH, "dir1", "subdirectory") in paths)
        self.assertTrue(os.path.join(cwd, BASEPATH, "dir2") in paths)
        self.assertTrue(os.path.join(cwd, BASEPATH, "dir3") in paths)
        self.assertTrue(os.path.join(cwd, BASEPATH, ".dir4") in paths)

        paths = find_paths(BASEPATH, just_files=True, abspath=True)
        self.assertEqual(18, len(paths))
        self.assertTrue(os.path.join(cwd, BASEPATH, "python_logo.png") in paths)

    def test_depth(self):
        """Only descend a certain depth into a tree."""
        paths = find_paths(BASEPATH, filter=DirectoryFilter(), depth=1)
        self.assertEqual(4, len(paths))
        self.assertTrue(os.path.join(BASEPATH, "dir1") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir2") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir3") in paths)
        self.assertTrue(os.path.join(BASEPATH, ".dir4") in paths)

        paths = find_paths(BASEPATH, filter=DirectoryFilter(), depth=2)
        self.assertEqual(5, len(paths))
        self.assertTrue(os.path.join(BASEPATH, "dir1", "subdirectory") in paths)

    def test_size(self):
        """Find files based on size criteria."""
        # all files except the image files are less than 10 bytes
        p_filter = SizeFilter(max_bytes=0)
        paths = walk_and_filter(BASEPATH, p_filter)
        self.assertEqual(12, len(paths))

        # only the image files contain data
        p_filter = SizeFilter(min_bytes=1)
        paths = walk_and_filter(BASEPATH, p_filter)
        self.assertEqual(6, len(paths))

        # three images between 450 bytes and 9000
        p_filter = SizeFilter(min_bytes=450, max_bytes=9000)
        paths = walk_and_filter(BASEPATH, p_filter)
        self.assertEqual(3, len(paths))

    def test_image(self):
        """Find all images."""
        image_filter = ImageFilter()
        paths = walk_and_filter(BASEPATH, image_filter)
        self.assertEqual(6, len(paths))

    def test_find_filepath(self):
        """Test when the root path to a find is a file and not a directory."""
        a_paths = find_paths(os.path.join(BASEPATH, "python_logo.png"), just_files=True)
        b_paths = find_paths(BASEPATH, just_files=True)
        self.assertEqual(a_paths, b_paths)

    try:
        import PIL

        def test_image_dimension(self):
            """Find images based on dimensions."""
            p_filter = ImageDimensionFilter(
                max_width=1000, max_height=1000, min_height=20, min_width=20
            )
            paths = walk_and_filter(BASEPATH, p_filter)
            self.assertEqual(6, len(paths))

            # ignore the 24x24
            p_filter = ImageDimensionFilter(
                max_width=1000, max_height=1000, min_height=25, min_width=25
            )
            paths = walk_and_filter(BASEPATH, p_filter)
            self.assertEqual(5, len(paths))

            # no 24x24, but only check it based on height
            p_filter = ImageDimensionFilter(min_height=25)
            paths = walk_and_filter(BASEPATH, p_filter)
            self.assertEqual(5, len(paths))

            # only the 24x24
            p_filter = ImageDimensionFilter(max_width=24, max_height=24)
            paths = walk_and_filter(BASEPATH, p_filter)
            self.assertEqual(1, len(paths))

            # only the 24x24, but only check it based on height
            p_filter = ImageDimensionFilter(max_height=24)
            paths = walk_and_filter(BASEPATH, p_filter)
            self.assertEqual(1, len(paths))

            # no parameters - all images
            p_filter = ImageDimensionFilter()
            paths = walk_and_filter(BASEPATH, p_filter)
            self.assertEqual(6, len(paths))

        def test_bw_image(self):
            """Find all grey scale images."""
            p_filter = GreyscaleImageFilter()
            paths = walk_and_filter(BASEPATH, p_filter)
            self.assertEqual(4, len(paths))

        def test_color_image(self):
            """Find all color images."""
            p_filter = ColorImageFilter()
            paths = walk_and_filter(BASEPATH, p_filter)
            self.assertEqual(2, len(paths))

    except ImportError:
        pass

    def test_generator(self):
        """Test with no parameters."""
        # find all paths
        paths = []
        for path in find_paths(BASEPATH):
            paths.append(path)
        self.assertEqual(23, len(paths))
        self.assertTrue(os.path.join(BASEPATH, "dir1") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir1", "subdirectory") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir2") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir3") in paths)
        self.assertTrue(os.path.join(BASEPATH, ".dir4") in paths)
        self.assertTrue(os.path.join(BASEPATH, "file1.txt") in paths)
        self.assertTrue(os.path.join(BASEPATH, "file2.dat") in paths)
        self.assertTrue(os.path.join(BASEPATH, "file3.txt") in paths)
        self.assertTrue(os.path.join(BASEPATH, "python_logo.gif") in paths)
        self.assertTrue(os.path.join(BASEPATH, "python_logo.png") in paths)
        self.assertTrue(os.path.join(BASEPATH, "python_logo_gs.gif") in paths)
        self.assertTrue(os.path.join(BASEPATH, "python_logo_gs.jpg") in paths)
        self.assertTrue(os.path.join(BASEPATH, "python_logo_gs.png") in paths)
        self.assertTrue(os.path.join(BASEPATH, "transparent_gs.png") in paths)
        self.assertTrue(
            os.path.join(BASEPATH, "dir1", "subdirectory", "sub.txt") in paths
        )
        self.assertTrue(os.path.join(BASEPATH, "dir1", "file4.txt") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir1", "file5.log") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir2", "file6.log") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir2", "file7.html") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir3", "file8") in paths)
        self.assertTrue(os.path.join(BASEPATH, "dir3", ".file9") in paths)
        self.assertTrue(os.path.join(BASEPATH, ".dir4", "file10") in paths)
        self.assertTrue(os.path.join(BASEPATH, ".dir4", "file20.txt") in paths)

    def test_path_does_not_exist(self):
        """Test when the parameter is a non-existent path."""
        # only find directories
        with self.assertRaises(EnvironmentError):
            find_paths(
                os.path.join(os.path.dirname(BASEPATH), "doesnotexist"), just_dirs=True
            )
