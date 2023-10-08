# -*- coding: utf-8 -*-
"""pathfinder package."""

import os

from pathfinder import filters


def walk_and_filter(filepath, pathfilter, ignore=None, abspath=None, depth=None):
    """Walk the file tree and filter it's contents."""
    if not os.path.exists(filepath):
        raise EnvironmentError(filepath)
    return list(walk_and_filter_generator(filepath, pathfilter, ignore, abspath, depth))


def walk_and_filter_generator(  # noqa:C901
    filepath, pathfilter, ignore=None, abspath=None, depth=None
):
    """
    Walk the file tree and filter it's contents.

    To ignore any paths an specify an ignore filter.

    To return absolute paths pass True for the abspath parameter.

    To limit how deep into the tree you travel, specify the depth parameter.
    """
    # by default no depth limit is enforced
    depth = -1 if depth is None else int(depth)
    if abspath is None:
        abspath = False

    base_path = _get_base_path(filepath)

    for root, dirs, files in os.walk(base_path):
        # descend the tree to a certain depth
        if _is_not_accepted_depth(root, base_path, depth):
            break

        yield from _process_tree(
            dirs, ignore, root, pathfilter, abspath, base_path, files
        )


def _process_tree(dirs, ignore, root, pathfilter, abspath, base_path, files):
    """Process the files and dirs."""
    # process in order
    ignored = []
    dirs.reverse()
    for adir in dirs:
        dirpath = os.path.normpath(os.path.join(root, adir))
        if ignore and ignore.accepts(dirpath):
            ignored.append(adir)
        else:
            yield from _assert_dir(pathfilter, dirpath, abspath, base_path)
    # remove the dirs we are ignoring
    for adir in ignored:
        dirs.remove(adir)

    for afile in files:
        filepath = os.path.normpath(os.path.join(root, afile))
        if not (ignore and ignore.accepts(filepath)):
            yield from _assert_file(pathfilter, filepath, abspath)


def _is_not_accepted_depth(root, base_path, depth):
    """Return if current level is past the accepted depth."""
    level = len(root.split(base_path)[1].split(os.sep))
    return level > depth and depth != -1


def _assert_dir(pathfilter, dirpath, abspath, base_path):
    """Assert the directory."""
    if pathfilter.accepts(dirpath):
        yield os.path.abspath(dirpath) if abspath else os.path.join(base_path, dirpath)


def _assert_file(pathfilter, filepath, abspath):
    """Assert the file."""
    if pathfilter.accepts(filepath):
        if abspath:
            filepath = os.path.abspath(filepath)
        yield filepath


def _get_base_path(filepath):
    """
    Return the directory for filepath.
    
    If filepath is a directory return that path.
    """
    return (
        os.path.normpath(filepath)
        if os.path.isdir(filepath)
        else os.path.normpath(os.path.dirname(filepath))
    )


def find_paths(
    directory_path,
    just_dirs=None,
    just_files=None,
    regex=None,
    fnmatch=None,
    filter=None,  # skipcq: PYL-W0622
    ignore=None,
    abspath=None,
    depth=None,
):
    """Find paths in the tree rooted at filepath."""
    if just_dirs:
        path_filter = filters.DirectoryFilter()
    elif just_files:
        path_filter = filters.FileFilter()
    elif regex:
        path_filter = filters.RegexFilter(regex)
    elif fnmatch:
        path_filter = filters.FnmatchFilter(fnmatch)
    elif not filter:
        path_filter = filters.AlwaysAcceptFilter()
    else:
        path_filter = filter

    return walk_and_filter(directory_path, path_filter, ignore, abspath, depth)
