import unittest

from ubuntucleaner.utils.files import filesizeformat


class TestFilesModule(unittest.TestCase):

    def test_filesizeformat(self):
        self.assertEqual(filesizeformat(None), "0 bytes")
        self.assertEqual(filesizeformat(0), "0 bytes")
        self.assertEqual(filesizeformat(1), "1 byte")
        self.assertEqual(filesizeformat(2), "2 bytes")
        self.assertEqual(filesizeformat(1024), "1.0 KB")
        self.assertEqual(filesizeformat(1024**2), "1.0 MB")
        self.assertEqual(filesizeformat(1024**3), "1.0 GB")
