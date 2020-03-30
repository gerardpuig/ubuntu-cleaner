import unittest

import mock
from ubuntucleaner.janitor.oldkernel_plugin import OldKernelPlugin


class TestOldKernelPlugin(unittest.TestCase):
    def setUp(self):
        self.oldkernel_plugin = OldKernelPlugin()
        self.oldkernel_plugin.current_kernel_version = '2.6.38-10'

    def test_is_old_kernel_package(self):
        self.assertEqual(self.oldkernel_plugin.p_kernel_version.findall('3.6.0-030600rc3')[0], '3.6.0-030600')
        self.assertEqual(self.oldkernel_plugin.p_kernel_version.findall('3.6.0-0306rc3')[0], '3.6.0-0306')
        self.assertEqual(self.oldkernel_plugin.p_kernel_version.findall('3.6.0-03rc3')[0], '3.6.0-03')

        self.assertTrue(self.oldkernel_plugin.is_old_kernel_package('linux-headers-2.6.35-28'))
        self.assertTrue(self.oldkernel_plugin.is_old_kernel_package('linux-image-2.6.38-9-generic'))
        self.assertFalse(self.oldkernel_plugin.is_old_kernel_package('linux-image-2.6.38-10'))
        self.assertFalse(self.oldkernel_plugin.is_old_kernel_package('linux-image-2.6.38-11'))

    @mock.patch('os.uname', mock.Mock(side_effect=Exception))
    def test_init_exception(self):
        plugin = OldKernelPlugin()
        self.assertEqual(plugin.current_kernel_version, 'undefined')

    def test_get_cruft(self):
        mocked_emit = mock.Mock()

        with mock.patch.object(OldKernelPlugin, 'emit', mocked_emit):
            self.oldkernel_plugin.get_cruft()

        mocked_emit.assert_called_with('scan_finished', True, mocked_emit.call_count - 1, 0)

    @mock.patch('ubuntucleaner.janitor.oldkernel_plugin.OldKernelPlugin.is_old_kernel_package',
                mock.Mock(side_effect=Exception))
    def test_get_cruft_exception(self):
        mocked_traceback = mock.Mock()

        with mock.patch('ubuntucleaner.janitor.oldkernel_plugin.get_traceback', mocked_traceback):
            self.oldkernel_plugin.get_cruft()

        mocked_traceback.assert_called_once_with()

    def test_get_summary(self):
        self.assertEqual(
            self.oldkernel_plugin.get_summary(1),
            '[1] Old Kernel'
        )

    def test_get_summary_empty(self):
        self.assertEqual(
            self.oldkernel_plugin.get_summary(0),
            'Old Kernel Packages (No old kernel package to be removed)'
        )
