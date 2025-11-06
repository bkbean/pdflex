import pytest
from pdflex import get_file_type


@pytest.mark.parametrize("a, expected", [
    ('file.pdf', 'pdf'),
    ('a/b/c.jpg', 'jpg'),
    ('/a/b/c.jpg', 'jpg'),
    ('a/b/c.', ''),
    ('a/b/c', ''),
    ('a/b/c/', ''),
    ('a/b/c////', ''),
    ('////a///b/c.', ''),
    (r'\a\b\c.pdf', 'pdf'),
])

def test_get_file_type(a, expected):
    result = get_file_type(a)
    assert result == expected