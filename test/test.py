import os
from pathfinder import pathfind, AndFilter, DirectoryFilter, DotDirectoryFilter, FnmatchFilter, RegexFilter, OrFilter, NotFilter

def test_just_dirs():
    basepath = "test/data"
    
    paths = pathfind(basepath, just_dirs=True)
    
    assert len(paths) == 4
    
    assert 'test/data/dir1' in paths
    assert 'test/data/dir2' in paths
    assert 'test/data/dir3' in paths
    assert 'test/data/.dir4' in paths

def test_just_files():
    basepath = "test/data"

    paths = pathfind(basepath, just_files=True)

    assert len(paths) == 10

    assert 'test/data/file1.txt' in paths
    assert 'test/data/file2.dat' in paths
    assert 'test/data/file3.txt' in paths
    assert 'test/data/dir1/file4.txt' in paths
    assert 'test/data/dir1/file5.log' in paths
    assert 'test/data/dir2/file6.log' in paths
    assert 'test/data/dir2/file7.html' in paths
    assert 'test/data/dir3/file8' in paths
    assert 'test/data/dir3/.file9' in paths
    assert 'test/data/.dir4/file10' in paths

def test_regex():
    basepath = "test/data"

    paths = pathfind(basepath, regex=".*")

    assert len(paths) == 14

    assert 'test/data/dir1' in paths
    assert 'test/data/dir2' in paths
    assert 'test/data/dir3' in paths
    assert 'test/data/.dir4' in paths
    assert 'test/data/file1.txt' in paths
    assert 'test/data/file2.dat' in paths
    assert 'test/data/file3.txt' in paths
    assert 'test/data/dir1/file4.txt' in paths
    assert 'test/data/dir1/file5.log' in paths
    assert 'test/data/dir2/file6.log' in paths
    assert 'test/data/dir2/file7.html' in paths
    assert 'test/data/dir3/file8' in paths
    assert 'test/data/dir3/.file9' in paths
    assert 'test/data/.dir4/file10' in paths


    paths = pathfind(basepath, regex=".*\..*t.*$")

    assert len(paths) == 5

    assert 'test/data/file1.txt' in paths
    assert 'test/data/file2.dat' in paths
    assert 'test/data/file3.txt' in paths
    assert 'test/data/dir1/file4.txt' in paths
    assert 'test/data/dir2/file7.html' in paths

    paths = pathfind(basepath, regex=".*1.*")

    assert len(paths) == 5

    assert 'test/data/dir1' in paths
    assert 'test/data/file1.txt' in paths
    assert 'test/data/dir1/file4.txt' in paths
    assert 'test/data/dir1/file5.log' in paths
    assert 'test/data/.dir4/file10' in paths

def test_fnmatch():
    basepath = "test/data"

    paths = pathfind(basepath, fnmatch="*")

    assert len(paths) == 14

    assert 'test/data/dir1' in paths
    assert 'test/data/dir2' in paths
    assert 'test/data/dir3' in paths
    assert 'test/data/.dir4' in paths
    assert 'test/data/file1.txt' in paths
    assert 'test/data/file2.dat' in paths
    assert 'test/data/file3.txt' in paths
    assert 'test/data/dir1/file4.txt' in paths
    assert 'test/data/dir1/file5.log' in paths
    assert 'test/data/dir2/file6.log' in paths
    assert 'test/data/dir2/file7.html' in paths
    assert 'test/data/dir3/file8' in paths
    assert 'test/data/dir3/.file9' in paths
    assert 'test/data/.dir4/file10' in paths

    paths = pathfind(basepath, fnmatch="*.txt")

    assert len(paths) == 3

    assert 'test/data/file1.txt' in paths
    assert 'test/data/file3.txt' in paths
    assert 'test/data/dir1/file4.txt' in paths

def test_all():
    basepath = "test/data"

    paths = pathfind(basepath)

    assert len(paths) == 14

    assert 'test/data/dir1' in paths
    assert 'test/data/dir2' in paths
    assert 'test/data/dir3' in paths
    assert 'test/data/.dir4' in paths
    assert 'test/data/file1.txt' in paths
    assert 'test/data/file2.dat' in paths
    assert 'test/data/file3.txt' in paths
    assert 'test/data/dir1/file4.txt' in paths
    assert 'test/data/dir1/file5.log' in paths
    assert 'test/data/dir2/file6.log' in paths
    assert 'test/data/dir2/file7.html' in paths
    assert 'test/data/dir3/file8' in paths
    assert 'test/data/dir3/.file9' in paths
    assert 'test/data/.dir4/file10' in paths
    
def test_and():
    basepath = "test/data"

    f = AndFilter(DirectoryFilter(), RegexFilter('.*2.*'))

    paths = pathfind(basepath, filter=f)
    
    assert len(paths) == 1

    assert 'test/data/dir2' in paths

def test_or():
    basepath = "test/data"

    f = OrFilter(DirectoryFilter(), RegexFilter('.*2.*'))

    paths = pathfind(basepath, filter=f)

    assert len(paths) == 7

    assert 'test/data/dir1' in paths
    assert 'test/data/dir2' in paths
    assert 'test/data/dir3' in paths
    assert 'test/data/.dir4' in paths
    assert 'test/data/file2.dat' in paths
    assert 'test/data/dir2/file6.log' in paths
    assert 'test/data/dir2/file7.html' in paths

def test_not():
    basepath = "test/data"

    f = AndFilter(NotFilter(FnmatchFilter('*3.txt')), FnmatchFilter('*.txt'))

    paths = pathfind(basepath, filter=f)

    assert len(paths) == 2

    assert 'test/data/file1.txt' in paths
    assert 'test/data/dir1/file4.txt' in paths

def test_ignore():
    basepath = "test/data"

    f = OrFilter(DirectoryFilter(), RegexFilter('.*2.*'))
    ignore = DotDirectoryFilter()
    paths = pathfind(basepath, filter=f, ignore=ignore)

    assert len(paths) == 6

    assert 'test/data/dir1' in paths
    assert 'test/data/dir2' in paths
    assert 'test/data/dir3' in paths
    assert 'test/data/file2.dat' in paths
    assert 'test/data/dir2/file6.log' in paths
    assert 'test/data/dir2/file7.html' in paths

def test_abspath():
    cwd = os.getcwd()
    basepath = "test/data"
    paths = pathfind(basepath, filter=DirectoryFilter(), abspath=True)
    assert len(paths) == 4

    assert os.path.join(cwd, 'test/data/dir1') in paths
    assert os.path.join(cwd, 'test/data/dir2') in paths
    assert os.path.join(cwd, 'test/data/dir3') in paths
    assert os.path.join(cwd, 'test/data/.dir4') in paths
    
if __name__ == "__main__":
    import sys
    import traceback
    
    tests = [a for a in dir() if a[0:4] == 'test']
    attrs = locals()
    for test in tests:
        print test.ljust(30, '.'),
        try:
            attrs[test]()
            print "OK"
        except AssertionError, e:
            print "ERROR"
            traceback.print_exc(file=sys.stdout)
            print
        except Exception, exp:
            print "FAIL"
            traceback.print_exc(file=sys.stdout)
            print