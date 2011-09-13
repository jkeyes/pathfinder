"""
pathfinder - making it easy to find paths
"""
import fnmatch
import os
import re

class AlwaysAcceptFilter(object):
    """ Accept every path. """

    def accepts(self, _):
        """ Always returns True. """
        return True
        
class DirectoryFilter(object):
    """ Accept directory paths. """

    def accepts(self, filepath):
        """ Returns True if filepath represents a directory. """
        return os.path.isdir(filepath)

class FileFilter(object):
    """ Accept file paths. """

    def accepts(self, filepath):
        """ Returns True if filepath represents a file. """
        return os.path.isfile(filepath)

class RegexFilter(object):
    """ Accept paths if they match the specified regular expression. """

    def __init__(self, regex):
        """ Initialize the filter with the specified regular expression. """
        super(RegexFilter, self).__init__()
        self.regex = re.compile(regex)

    def accepts(self, filepath):
        """ Returns True if the regular expression matches the filepath. """
        return self.regex.match(filepath) is not None
    
class FnmatchFilter(object):
    """ Accept paths if they match the specifed fnmatch pattern. """

    def __init__(self, pattern):
        """ Initialize the filter with the specified fnmatch pattern. """
        super(FnmatchFilter, self).__init__()
        self.pattern = pattern

    def accepts(self, filepath):
        """ Returns True if the fnmatch pattern matches the filepath. """
        return fnmatch.fnmatch(filepath, self.pattern)
    
class AndFilter(list):
    """ Accept paths if all of it's filters accept the path. """

    def __init__(self, *args):
        """ Initialize the filter with the list of filters. """
        list.__init__(self, args)

    def accepts(self, filepath):
        """ Returns True if all of the filters in this filter return True. """
        result = True
        for sub_filter in self:
            result = result and sub_filter.accepts(filepath)
        return result

class OrFilter(list):
    """ Accept paths if any of it's filters accept the path. """

    def __init__(self, *args):
        """ Initialize the filter with the list of filters. """
        list.__init__(self, args)

    def accepts(self, filepath):
        """ Returns True if any of the filters in this filter return True. """
        result = False
        for sub_filter in self:
            result = result or sub_filter.accepts(filepath)
        return result

class NotFilter(object):
    """ Negate the accept of the specified filter. """

    def __init__(self, pathfilter):
        """ Initialize the filter with the filter it is to negate. """
        super(NotFilter, self).__init__()
        self.pathfilter = pathfilter

    def accepts(self, filepath):
        """ Returns True of the sub-filter returns False. """
        return not self.pathfilter.accepts(filepath)

class DotDirectoryFilter(object):
    """ Do not accept a path for a directory that begins with a period. """

    def __init__(self):
        """ 
        Initialise the filter to ignore directories beginning with
        a period.
        """
        self.filter = AndFilter(
                DirectoryFilter(), 
                RegexFilter(r'.*%s*\..*$' % (os.sep)))

    def accepts(self, filepath):
        """
        Return True if the filepath is not a directory beginning with
        a period.
        """
        return self.filter.accepts(filepath)
    
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

    result = []
    pwd = os.getcwd()
    if os.path.isdir(filepath):
        base_path = os.path.normpath(filepath)
    else:
        base_path = os.path.normpath(os.path.dirname(filepath))

    os.chdir(base_path)
    for root, dirs, files in os.walk('.'):
        
        # descend the tree to a certain depth
        level = len(root.split(os.sep))
        if level > depth and depth != -1:
            break
        
        # process in order
        dirs.reverse()
        for adir in dirs:
            dirpath = os.path.normpath(os.path.join(root, adir))
            if ignore and ignore.accepts(dirpath):
                dirs.remove(adir)
            else:
                if pathfilter.accepts(dirpath):
                    if abspath:
                        result.append(os.path.abspath(dirpath))
                    else:
                        result.append(os.path.join(base_path, dirpath))
        for afile in files:
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
