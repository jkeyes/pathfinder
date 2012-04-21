"""
pathfinder tests
"""

import os
from os.path import join
from pathfinder import pathfind
from pathfinder import AndFilter
from pathfinder import DirectoryFilter
from pathfinder import DotDirectoryFilter
from pathfinder import FnmatchFilter
from pathfinder import RegexFilter
from pathfinder import OrFilter
from pathfinder import NotFilter

BASEPATH = join("test", "data")

def test_just_dirs():
    """ Test just_dirs parameter."""
    # only find directories
    paths = pathfind(BASEPATH, just_dirs=True)
    assert len(paths) == 5
    assert join(BASEPATH, 'dir1') in paths
    assert join(BASEPATH, 'dir1', 'subdirectory') in paths
    assert join(BASEPATH, 'dir2') in paths
    assert join(BASEPATH, 'dir3') in paths
    assert join(BASEPATH, '.dir4') in paths

def test_just_files():
    """ Test just_files parameter."""
    # only find files
    paths = pathfind(BASEPATH, just_files=True)
    assert len(paths) == 11
    assert join(BASEPATH, 'file1.txt') in paths
    assert join(BASEPATH, 'file2.dat') in paths
    assert join(BASEPATH, 'file3.txt') in paths
    assert join(BASEPATH, 'dir1', 'subdirectory', 'sub.txt') in paths
    assert join(BASEPATH, 'dir1', 'file4.txt') in paths
    assert join(BASEPATH, 'dir1', 'file5.log') in paths
    assert join(BASEPATH, 'dir2', 'file6.log') in paths
    assert join(BASEPATH, 'dir2', 'file7.html') in paths
    assert join(BASEPATH, 'dir3', 'file8') in paths
    assert join(BASEPATH, 'dir3', '.file9') in paths
    assert join(BASEPATH, '.dir4', 'file10') in paths

def test_regex():
    """ Test regex parameter."""
    # find all files and directories
    paths = pathfind(BASEPATH, regex=".*")
    assert len(paths) == 16
    assert join(BASEPATH, 'dir1') in paths
    assert join(BASEPATH, 'dir1', 'subdirectory') in paths
    assert join(BASEPATH, 'dir2') in paths
    assert join(BASEPATH, 'dir3') in paths
    assert join(BASEPATH, '.dir4') in paths
    assert join(BASEPATH, 'file1.txt') in paths
    assert join(BASEPATH, 'file2.dat') in paths
    assert join(BASEPATH, 'file3.txt') in paths
    assert join(BASEPATH, 'dir1', 'subdirectory', 'sub.txt') in paths
    assert join(BASEPATH, 'dir1', 'file4.txt') in paths
    assert join(BASEPATH, 'dir1', 'file5.log') in paths
    assert join(BASEPATH, 'dir2', 'file6.log') in paths
    assert join(BASEPATH, 'dir2', 'file7.html') in paths
    assert join(BASEPATH, 'dir3', 'file8') in paths
    assert join(BASEPATH, 'dir3', '.file9') in paths
    assert join(BASEPATH, '.dir4', 'file10') in paths

    # find only files and directories with a t in the extension
    paths = pathfind(BASEPATH, regex=".*\..*t.*$")
    assert len(paths) == 6
    assert join(BASEPATH, 'file1.txt') in paths
    assert join(BASEPATH, 'file2.dat') in paths
    assert join(BASEPATH, 'file3.txt') in paths
    assert join(BASEPATH, 'dir1', 'subdirectory', 'sub.txt') in paths
    assert join(BASEPATH, 'dir1', 'file4.txt') in paths
    assert join(BASEPATH, 'dir2', 'file7.html') in paths

    # find only files and directories with 1 anywhere in the path
    paths = pathfind(BASEPATH, regex=".*1.*")
    assert len(paths) == 7
    assert join(BASEPATH, 'dir1') in paths
    assert join(BASEPATH, 'file1.txt') in paths
    assert join(BASEPATH, 'dir1', 'subdirectory') in paths
    assert join(BASEPATH, 'dir1', 'subdirectory', 'sub.txt') in paths
    assert join(BASEPATH, 'dir1', 'file4.txt') in paths
    assert join(BASEPATH, 'dir1', 'file5.log') in paths
    assert join(BASEPATH, '.dir4', 'file10') in paths

def test_fnmatch():
    """ Test fnmatch parameter."""
    # find all files and directories
    paths = pathfind(BASEPATH, fnmatch="*")
    assert len(paths) == 16
    assert join(BASEPATH, 'dir1') in paths
    assert join(BASEPATH, 'dir1', 'subdirectory') in paths
    assert join(BASEPATH, 'dir2') in paths
    assert join(BASEPATH, 'dir3') in paths
    assert join(BASEPATH, '.dir4') in paths
    assert join(BASEPATH, 'file1.txt') in paths
    assert join(BASEPATH, 'file2.dat') in paths
    assert join(BASEPATH, 'file3.txt') in paths
    assert join(BASEPATH, 'dir1', 'subdirectory', 'sub.txt') in paths
    assert join(BASEPATH, 'dir1', 'file4.txt') in paths
    assert join(BASEPATH, 'dir1', 'file5.log') in paths
    assert join(BASEPATH, 'dir2', 'file6.log') in paths
    assert join(BASEPATH, 'dir2', 'file7.html') in paths
    assert join(BASEPATH, 'dir3', 'file8') in paths
    assert join(BASEPATH, 'dir3', '.file9') in paths
    assert join(BASEPATH, '.dir4', 'file10') in paths

    # find only files or directories with a .txt extension
    paths = pathfind(BASEPATH, fnmatch="*.txt")
    assert len(paths) == 4
    assert join(BASEPATH, 'file1.txt') in paths
    assert join(BASEPATH, 'file3.txt') in paths
    assert join(BASEPATH, 'dir1', 'subdirectory', 'sub.txt') in paths
    assert join(BASEPATH, 'dir1', 'file4.txt') in paths

def test_all():
    """ Test with no parameters. """
    # find all paths
    paths = pathfind(BASEPATH)
    assert len(paths) == 16
    assert join(BASEPATH, 'dir1') in paths
    assert join(BASEPATH, 'dir1', 'subdirectory') in paths
    assert join(BASEPATH, 'dir2') in paths
    assert join(BASEPATH, 'dir3') in paths
    assert join(BASEPATH, '.dir4') in paths
    assert join(BASEPATH, 'file1.txt') in paths
    assert join(BASEPATH, 'file2.dat') in paths
    assert join(BASEPATH, 'file3.txt') in paths
    assert join(BASEPATH, 'dir1', 'subdirectory', 'sub.txt') in paths
    assert join(BASEPATH, 'dir1', 'file4.txt') in paths
    assert join(BASEPATH, 'dir1', 'file5.log') in paths
    assert join(BASEPATH, 'dir2', 'file6.log') in paths
    assert join(BASEPATH, 'dir2', 'file7.html') in paths
    assert join(BASEPATH, 'dir3', 'file8') in paths
    assert join(BASEPATH, 'dir3', '.file9') in paths
    assert join(BASEPATH, '.dir4', 'file10') in paths
    
def test_and():
    """ Test AndFilter."""
    # find directories with a 2 anywhere in the path
    filt = AndFilter(DirectoryFilter(), RegexFilter('.*2.*'))
    paths = pathfind(BASEPATH, filter=filt)
    assert len(paths) == 1
    assert join(BASEPATH, 'dir2') in paths

def test_or():
    """ Test OrFilter."""
    # find all directories and any files (or directories)
    # with 2 in the path
    filt = OrFilter(DirectoryFilter(), RegexFilter('.*2.*'))
    paths = pathfind(BASEPATH, filter=filt)
    assert len(paths) == 8
    assert join(BASEPATH, 'dir1') in paths
    assert join(BASEPATH, 'dir1', 'subdirectory') in paths
    assert join(BASEPATH, 'dir2') in paths
    assert join(BASEPATH, 'dir3') in paths
    assert join(BASEPATH, '.dir4') in paths
    assert join(BASEPATH, 'file2.dat') in paths
    assert join(BASEPATH, 'dir2', 'file6.log') in paths
    assert join(BASEPATH, 'dir2', 'file7.html') in paths

def test_not():
    """ Test NotFilter."""
    # find all files and directories with a .txt extension
    # except ones that end in 3.txt
    filt = AndFilter(NotFilter(FnmatchFilter('*3.txt')), FnmatchFilter('*.txt'))
    paths = pathfind(BASEPATH, filter=filt)
    assert len(paths) == 3
    assert join(BASEPATH, 'file1.txt') in paths
    assert join(BASEPATH, 'dir1', 'subdirectory', 'sub.txt') in paths
    assert join(BASEPATH, 'dir1', 'file4.txt') in paths

def test_ignore():
    """ Test ignore parameter."""
    # find all directories and all files and directories 
    # with a 2 in the path and no directories that begin
    # with a dot
    filt = OrFilter(DirectoryFilter(), RegexFilter('.*2.*'))
    ignore = DotDirectoryFilter()
    paths = pathfind(BASEPATH, filter=filt, ignore=ignore)
    assert len(paths) == 7
    assert join(BASEPATH, 'dir1') in paths
    assert join(BASEPATH, 'dir1', 'subdirectory') in paths
    assert join(BASEPATH, 'dir2') in paths
    assert join(BASEPATH, 'dir3') in paths
    assert join(BASEPATH, 'file2.dat') in paths
    assert join(BASEPATH, 'dir2', 'file6.log') in paths
    assert join(BASEPATH, 'dir2', 'file7.html') in paths

def test_abspath():
    """ Test abspath parameter."""
    # test that absolute paths are returned
    cwd = os.getcwd()
    paths = pathfind(BASEPATH, filter=DirectoryFilter(), abspath=True)
    assert len(paths) == 5
    assert join(cwd, BASEPATH, 'dir1') in paths
    assert join(cwd, BASEPATH, 'dir1', 'subdirectory') in paths
    assert join(cwd, BASEPATH, 'dir2') in paths
    assert join(cwd, BASEPATH, 'dir3') in paths
    assert join(cwd, BASEPATH, '.dir4') in paths

def test_depth():
    """ Test depth parameter."""
    # only descend the tree to one level of subdirectories
    paths = pathfind(BASEPATH, filter=DirectoryFilter(), depth=1)
    assert len(paths) == 4
    assert join(BASEPATH, 'dir1') in paths
    assert join(BASEPATH, 'dir2') in paths
    assert join(BASEPATH, 'dir3') in paths
    assert join(BASEPATH, '.dir4') in paths

    paths = pathfind(BASEPATH, filter=DirectoryFilter(), depth=2)
    assert len(paths) == 5
    assert join(BASEPATH, 'dir1', 'subdirectory') in paths
