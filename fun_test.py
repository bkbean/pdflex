import unittest
from parameterized import parameterized
from func import get_file_type


# 编写参数化测试用例
class TestFunctions(unittest.TestCase):

    @parameterized.expand([
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
    def test_get_file_type(self, a, expected):
        result = get_file_type(a)
        self.assertEqual(result, expected)


# 运行测试
if __name__ == '__main__':
    unittest.main()