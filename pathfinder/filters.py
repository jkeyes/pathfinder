# -*- coding: utf-8 -*-
"""pathfinder - making it easy to find paths."""
import fnmatch as fnmatch_module
import os
import re
from math import sqrt


class Filter:
    """Base filter class."""

    def __and__(self, other):
        """Override dunder and."""
        return AndFilter(self, other)

    def __or__(self, other):
        """Override dunder or."""
        return OrFilter(self, other)

    def find(self, filepath):
        """Walk the directory and try to find the filepath."""
        from pathfinder import walk_and_filter

        return walk_and_filter(filepath, self)


class AlwaysAcceptFilter(Filter):
    """Accept every path."""

    def accepts(self, _):
        """Return True always."""
        return True


class DirectoryFilter(Filter):
    """Accept directory paths."""

    def accepts(self, filepath):
        """Return True if filepath represents a directory."""
        return os.path.isdir(filepath)


class FileFilter(Filter):
    """Accept file paths."""

    def accepts(self, filepath):
        """Return True if filepath represents a file."""
        return os.path.isfile(filepath)


class RegexFilter(Filter):
    """Accept paths if they match the specified regular expression."""

    def __init__(self, regex):
        """Initialize the filter with the specified regular expression."""
        super(RegexFilter, self).__init__()
        self.regex = re.compile(regex)

    def accepts(self, filepath):
        """Return True if the regular expression matches the filepath."""
        return self.regex.match(filepath) is not None


class FnmatchFilter(Filter):
    """Accept paths if they match the specifed fnmatch pattern."""

    def __init__(self, pattern):
        """Initialize the filter with the specified fnmatch pattern."""
        super(FnmatchFilter, self).__init__()
        self.pattern = pattern

    def accepts(self, filepath):
        """Return True if the fnmatch pattern matches the filepath."""
        return fnmatch_module.fnmatch(filepath, self.pattern)


class AndFilter(Filter, list):
    """Accept paths if all of it's filters accept the path."""

    def __init__(self, *args):
        """Initialize the filter with the list of filters."""
        list.__init__(self, args)

    def accepts(self, filepath):
        """Return True if all of the filters in this filter return True."""
        return all(sub_filter.accepts(filepath) for sub_filter in self)


class OrFilter(Filter, list):
    """Accept paths if any of it's filters accept the path."""

    def __init__(self, *args):
        """Initialize the filter with the list of filters."""
        list.__init__(self, args)

    def accepts(self, filepath):
        """Return True if any of the filters in this filter return True."""
        return any(sub_filter.accepts(filepath) for sub_filter in self)


class NotFilter(Filter):
    """Negate the accept of the specified filter."""

    def __init__(self, pathfilter):
        """Initialize the filter with the filter it is to negate."""
        super(NotFilter, self).__init__()
        self.pathfilter = pathfilter

    def accepts(self, filepath):
        """Return True of the sub-filter returns False."""
        return not self.pathfilter.accepts(filepath)


class DotDirectoryFilter(AndFilter):
    """Do not accept a path for a directory that begins with a period."""

    def __init__(self):
        """
        Initialise the filter.

        Ignore directories beginning with a period.
        """
        super(DotDirectoryFilter, self).__init__(
            DirectoryFilter(), RegexFilter(rf".*{os.sep}*\..*$")
        )


class SizeFilter(FileFilter):
    """Accept files within a min and/or max bytes range."""

    def __init__(self, max_bytes=None, min_bytes=None):
        """Initialise the size filter."""
        self.file_filter = FileFilter()
        self.max_bytes = max_bytes
        self.min_bytes = min_bytes

    def accepts(self, filepath):
        """Return True if the file size is within the range."""
        if super(SizeFilter, self).accepts(filepath):
            stat = os.stat(filepath)
            return self._has_gtr_min_bytes(stat) and self._has_lte_max_bytes(stat)
        return False

    def _has_lte_max_bytes(self, stat):
        """Return whether the file size is less than or equal to the max size."""
        return self.max_bytes is None or stat.st_size <= self.max_bytes

    def _has_gtr_min_bytes(self, stat):
        """Return whether the file size is greater than or equal to the min size."""
        return self.min_bytes is None or stat.st_size >= self.min_bytes


class ImageFilter(Filter):
    """Accept paths for Image files."""

    def __init__(self):
        """Initialise the image filter."""
        self.file_filter = OrFilter(
            FnmatchFilter("*.jpg"),
            FnmatchFilter("*.jpeg"),
            FnmatchFilter("*.png"),
            FnmatchFilter("*.gif"),
            FnmatchFilter("*.bmp"),
            FnmatchFilter("*.tiff"),
        )

    def accepts(self, filepath):
        """Return true if filepath has an image extension."""
        return self.file_filter.accepts(filepath)


class ImageDimensionFilter(ImageFilter):
    """Accept paths for Image files."""

    def __init__(
        self, max_width=None, max_height=None, min_width=None, min_height=None
    ):
        """Initialise the image dimension filter."""
        super(ImageDimensionFilter, self).__init__()

        if min_height is None:
            min_height = 0
        if min_width is None:
            min_width = 0

        self.max_width = max_width
        self.max_height = max_height
        self.min_width = min_width
        self.min_height = min_height

    def accepts(self, filepath):
        """Return True if filepath satisfies the image constraints."""
        if super(ImageDimensionFilter, self).accepts(filepath):
            if (
                self.min_height == 0
                and self.min_width == 0
                and self.max_height is None
                and self.max_width is None
            ):
                return True

            from PIL import Image

            image = Image.open(filepath)
            size = image.size
            if self.max_width and size[0] > self.max_width:
                return False
            if self.max_height and size[1] > self.max_height:
                return False
            if self.min_width and size[0] < self.min_width:
                return False
            if self.min_height and size[1] < self.min_height:
                return False
            return True
        return False


class GreyscaleImageFilter(ImageFilter):
    """Accept black and white images."""

    def accepts(self, filepath):
        """Return true if the file located at filepath is a greyscale image."""
        if super(GreyscaleImageFilter, self).accepts(filepath):
            from PIL import Image, ImageStat

            image = Image.open(filepath)
            palette = image.getpalette()

            if palette:
                # GIF support
                return is_greyscale_palette(palette)

            stat = ImageStat.Stat(image)
            # B&W JPEG: 8-bit pixels, black and white
            if image.mode == "L":
                return True
            # if the standard deviation of the mean is less than 1 we say it's a greyscale image
            # where mean = average (arithmetic mean) pixel level for each band in the image.
            # note we ignore alpha bands here
            return stdv(stat.mean[:3]) < 1
        return False


class ColorImageFilter(ImageFilter):
    """Accept colour images."""

    def accepts(self, filepath):
        """Return True if the file at filepath is a colour image."""
        if super(ColorImageFilter, self).accepts(filepath):
            from PIL import Image, ImageStat

            image = Image.open(filepath)
            palette = image.getpalette()

            if palette:
                # GIF SUPPORT
                return is_color_palette(palette)

            stat = ImageStat.Stat(image)
            # B&W JPEG: 8-bit pixels, black and white
            if image.mode == "L":
                return False

            # if the standard deviation of the mean is more than 1 we say it's a color image
            # where mean = average (arithmetic mean) pixel level for each band in the image.
            # note we ignore alpha bands here
            return stdv(stat.mean[:3]) > 1
        return False


def stdv(band_means):
    """Calculate the standard deviation of the image bands."""
    num_bands, _sum, mean, std = len(band_means), sum(band_means), 0, 0
    mean = _sum / float(num_bands)
    sum_diff = sum((a - mean) ** 2 for a in band_means)
    std = sqrt(sum_diff / float(num_bands - 1))
    return std


def is_greyscale_palette(palette):
    """Return whether the palette is greyscale only."""
    for i in range(256):
        j = i * 3
        if palette[j] != palette[j + 1] != palette[j + 2]:
            return False
    return True


def is_color_palette(palette):
    """Return whether the palette has color."""
    return not is_greyscale_palette(palette)
