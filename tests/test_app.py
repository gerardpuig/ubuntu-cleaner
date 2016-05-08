import unittest
from ubuntucleaner.main import UbuntuCleanerWindow


class TestApp(unittest.TestCase):
    def setUp(self):
        self.window = UbuntuCleanerWindow()

    def test_app(self):
        self.assertEqual(self.window.feature_dict, {'janitor': 0})
        self.assertIsNotNone(self.window.aboutdialog)

    def tearDown(self):
        del self.window
