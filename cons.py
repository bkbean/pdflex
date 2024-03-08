from enum import Enum

class RC(Enum):
    SUCCESS = 0
    NULL_INPUT = 1
    INVALID_INPUT = 2
    NULL_OUTPUT = 3
    INVALID_OUTPUT = 4


# PyMuPDF supports the following file types:
IFORMATS_DOC = ('pdf', 'xps', 'epub', 'mobi', 'fb2', 'cbz', 'svg', 'txt')
IFORMATS_IMG = ('jpg', 'jpeg', 'png', 'bmp', 'gif', 'tiff', 'pnm', 'pgm', 'pbm', 'ppm', 'pam', 'jxr', 'jpx', 'jp2', 'psd')
OFORMATS_IMG = ('jpg', 'jpeg', 'png', 'pnm', 'pgm', 'pbm', 'ppm', 'pam', 'psd', 'ps')