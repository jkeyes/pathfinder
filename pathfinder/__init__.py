#
# Copyright 2009 keyes.ie
#
# License: http://jkeyes.mit-license.org/
#

import os

from pathfinder.filters import *

def walk_and_filter(filepath, pathfilter, 
        ignore=None, abspath=None, depth=None):
    """ 
    Walk the file tree and filter it's contents. 
    
    To ignore any paths an specify an ignore filter.
    
    To return absolute paths pass True for the abspath parameter.
    
    To limit how deep into the tree you travel, specify the depth parameter.
    """
    # by default no depth limit is enforced
    if depth is None:
        depth = -1
    else:
        depth = int(depth)

    if abspath is None:
        abspath = False

    result = []
    pwd = os.getcwd()
    if os.path.isdir(filepath):
        base_path = os.path.normpath(filepath)
    else:
        base_path = os.path.normpath(os.path.dirname(filepath))

    os.chdir(base_path)
    for root, dirs, files in os.walk('.'):
        
        print "ROOT %s" % (root)
        print "DIRS %s" % (dirs)
        print "FILES %s" % (files)
        
        # descend the tree to a certain depth
        level = len(root.split(os.sep))
        if level > depth and depth != -1:
            break
        
        # process in order
        dirs.reverse()
        for adir in dirs:
            print "Testing ", adir
            dirpath = os.path.normpath(os.path.join(root, adir))
            print "        ", dirpath
            if ignore and ignore.accepts(dirpath):
                print "        ignore..."
                dirs.remove(adir)
            else:
                print "        test it..."
                if pathfilter.accepts(dirpath):
                    print "        accepted..."
                    if abspath:
                        result.append(os.path.abspath(dirpath))
                    else:
                        result.append(os.path.join(base_path, dirpath))
        for afile in files:
            print "Testing ", afile
            filepath = os.path.normpath(os.path.join(root, afile))
            if pathfilter.accepts(filepath):
                if abspath:
                    result.append(os.path.abspath(filepath))
                else:
                    result.append(os.path.join(base_path, filepath))
    os.chdir(pwd)
    return result
    
def pathfind(filepath, just_dirs=None, just_files=None, regex=None, \
            fnmatch=None, filter=None, ignore=None, abspath=None, depth=None):
    return find(filepath, just_dirs, just_files, regex, fnmatch,
            filter, ignore, abspath, depth)
    
def find(filepath, just_dirs=None, just_files=None, regex=None, \
            fnmatch=None, filter=None, ignore=None, abspath=None, depth=None):
    """
    Find paths in the tree rooted at filepath.
    """
    if just_dirs:
        filter = DirectoryFilter()
    elif just_files:
        filter = FileFilter()
    elif regex:
        filter = RegexFilter(regex)
    elif fnmatch:
        filter = FnmatchFilter(fnmatch)
    elif not filter:
        filter = AlwaysAcceptFilter()

    return walk_and_filter(filepath, filter, ignore, abspath, depth)
