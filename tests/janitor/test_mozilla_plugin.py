import os
import unittest

import mock
from ubuntucleaner.janitor.mozilla_plugin import FirefoxCachePlugin


class TestMozillaCachePlugin(unittest.TestCase):
    def setUp(self):
        self.firefox_plugin = FirefoxCachePlugin()

    def test_firefox_plugin(self):
        self.assertTrue(
            os.path.expanduser('~/.mozilla/firefox/5tzbwjwa.default'),
            self.firefox_plugin.get_path()
        )

    @mock.patch('ubuntucleaner.settings.common.RawConfigSetting.sections',
                mock.Mock(side_effect=Exception))
    def test_firefox_plugin_path_exception(self):
        self.assertTrue(
            os.path.expanduser('~/.mozilla/firefox/5tzbwjwa.default'),
            self.firefox_plugin.get_path()
        )
