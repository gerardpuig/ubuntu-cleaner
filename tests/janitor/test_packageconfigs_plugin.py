import unittest

from gi.repository import GdkPixbuf

import mock
from ubuntucleaner.janitor.packageconfigs_plugin import (PackageConfigObject,
                                                         PackageConfigsPlugin)


class TestPackageConfigObject(unittest.TestCase):
    def setUp(self):
        self.packageconfig = PackageConfigObject('test')

    def test_get_icon(self):
        self.assertTrue(type(self.packageconfig.get_icon()), GdkPixbuf.Pixbuf)

    def test_get_size_display(self):
        self.assertEqual(self.packageconfig.get_size_display(), '')

    def test_get_size(self):
        self.assertEqual(self.packageconfig.get_size(), 0)


class TestPackageConfigsPlugin(unittest.TestCase):
    def setUp(self):
        self.packageconfig_plugin = PackageConfigsPlugin()

    def test_get_cruft(self):
        with mock.patch.object(PackageConfigsPlugin, 'emit') as mocked_emit:
            self.packageconfig_plugin.get_cruft()

        mocked_emit.assert_called_with('scan_finished', True, mocked_emit.call_count - 1, 0)

    def test_clean_empty_cruft(self):
        mocked_emit = mock.Mock()

        with mock.patch.object(PackageConfigsPlugin, 'emit', mocked_emit):
            self.packageconfig_plugin.clean_cruft()

        mocked_emit.assert_called_with('all_cleaned', True)

    def test_get_summary(self):
        self.assertEqual(
            self.packageconfig_plugin.get_summary(1),
            '[1] Package Configs'
        )

    def test_get_summary_empty(self):
        self.assertEqual(
            self.packageconfig_plugin.get_summary(0),
            'Packages Configs (No package config to be removed)'
        )
