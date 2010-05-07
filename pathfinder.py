import fnmatch
import os
import re

class AlwaysAcceptFilter(object):

    def accepts(self, filepath):
        return True
        
class DirectoryFilter(object):

    def accepts(self, filepath):
        return os.path.isdir(filepath)

class FileFilter(object):

    def accepts(self, filepath):
        return os.path.isfile(filepath)

class RegexFilter(object):

    def __init__(self, regex):
        super(RegexFilter, self).__init__()
        self.regex = re.compile(regex)

    def accepts(self, filepath):
        return self.regex.match(filepath) is not None
    
class FnmatchFilter(object):

    def __init__(self, pattern):
        super(FnmatchFilter, self).__init__()
        self.pattern = pattern

    def accepts(self, filepath):
        return fnmatch.fnmatch(filepath, self.pattern)
    
class AndFilter(object):

    def __init__(self, *args):
        super(AndFilter, self).__init__()
        self.filters = args

    def accepts(self, filepath):
        result = True
        for filter in self.filters:
            result = result and filter.accepts(filepath)
        return result

class OrFilter(object):

    def __init__(self, *args):
        super(OrFilter, self).__init__()
        self.filters = args

    def accepts(self, filepath):
        result = False
        for filter in self.filters:
            result = result or filter.accepts(filepath)
        return result

class NotFilter(object):
    def __init__(self, pathfilter):
        super(NotFilter, self).__init__()
        self.pathfilter = pathfilter

    def accepts(self, filepath):
        return not self.pathfilter.accepts(filepath)

class DotDirectoryFilter(object):
    def __init__(self):
        self.filter = AndFilter(DirectoryFilter(), RegexFilter(r'.*/\..*$'))

    def accepts(self, filepath):
        return self.filter.accepts(filepath)
    
def walk_and_filter(filepath, pathfilter, ignore=None, abspath=None):
    result = []
    if os.path.isdir(filepath):
        base_path = os.path.normpath(filepath)
    else:
        base_path = os.path.normpath(os.path.dirname(filepath))
    for root, dirs, files in os.walk(base_path):
        dirs.reverse()
        for d in dirs:
            dirpath = os.path.join(root, d)
            
            if ignore and ignore.accepts(dirpath):
                dirs.remove(d)
            else:
                if pathfilter.accepts(dirpath):
                    if abspath:
                        result.append(os.path.abspath(dirpath))
                    else:
                        result.append(dirpath)
                        
        for f in files:
            filepath = os.path.join(root, f)
            if pathfilter.accepts(filepath):
                if abspath:
                    result.append(os.path.abspath(filepath))
                else:
                    result.append(filepath)
                    
    return result
    
    
def pathfind(filepath, just_dirs=None, just_files=None, regex=None, fnmatch=None, filter=None, ignore=None, abspath=None):
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

    return walk_and_filter(filepath, filter, ignore, abspath)
