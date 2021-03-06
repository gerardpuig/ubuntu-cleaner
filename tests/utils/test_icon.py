import unittest
import mock

from gi.repository import Gtk, GdkPixbuf
from ubuntucleaner.utils.icon import get_from_name, get_from_list, get_from_mime_type, get_from_file, DEFAULT_SIZE


def patch_load_icon(side_effect=None):
    return mock.patch(
        "ubuntucleaner.utils.icon.Gtk.IconTheme.load_icon",
        side_effect=side_effect)


def patch_log():
    return mock.patch("ubuntucleaner.utils.icon.log")


def patch_get_from_name():
    return mock.patch("ubuntucleaner.utils.icon.get_from_name")


def patch_get_from_list():
    return mock.patch("ubuntucleaner.utils.icon.get_from_list")


def patch_new_from_file_at_size():
    return mock.patch("ubuntucleaner.utils.icon.GdkPixbuf.Pixbuf.new_from_file_at_size")


class TestIconModule(unittest.TestCase):

    def test_get_from_name(self):
        """
        Calling with no parameters should return the pixbuf object through `load_icon()`
        and default parameters.
        """
        m_pixbuf = mock.Mock(spec=GdkPixbuf.Pixbuf, get_height=lambda: DEFAULT_SIZE)
        with patch_load_icon() as m_load_icon:
            m_load_icon.return_value = m_pixbuf
            pixbuf = get_from_name()
        self.assertEqual(
            m_load_icon.call_args_list, [mock.call("gtk-execute", 24, 0)]
        )
        self.assertEqual(pixbuf, m_pixbuf)

    def helper_test_get_from_name_force_reload(self, force_reload, call_args_list):
        """Helper for checking if `get_default()` is called or not based on `force_reload` value."""
        with mock.patch("ubuntucleaner.utils.icon.Gtk.IconTheme.get_default") as m_get_default:
            get_from_name(force_reload=force_reload)
        # resets `icontheme` global to unmocked version for subsequent tests
        get_from_name(force_reload=force_reload)
        self.assertEqual(m_get_default.call_args_list, call_args_list)

    def test_get_from_name_force_reload(self):
        """Setting `force_reload` should trigger another `get_default()` call."""
        self.helper_test_get_from_name_force_reload(True, [mock.call()])
        self.helper_test_get_from_name_force_reload(False, [])

    def helper_test_get_from_name_only_path(self, only_path, call_args_list):
        """Helper for checking if `lookup_icon()` is called or not based on `only_path` value."""
        with mock.patch("ubuntucleaner.utils.icon.Gtk.IconTheme.lookup_icon") as m_lookup_icon:
            get_from_name(only_path=True)
        self.assertEqual(
            m_lookup_icon.call_args_list,
            [mock.call("gtk-execute", 24, Gtk.IconLookupFlags.USE_BUILTIN)]
        )

    def test_get_from_name_only_path(self):
        """Setting `lookup_icon()` should only be caled when `only_path` is set."""
        self.helper_test_get_from_name_only_path(
            True,
            [mock.call("gtk-execute", 24, Gtk.IconLookupFlags.USE_BUILTIN)]
        )
        self.helper_test_get_from_name_only_path(False, [])

    def test_get_from_name_load_icon_exception(self):
        """On exception `load_icon()` should be called again."""
        m_pixbuf = mock.Mock(spec=GdkPixbuf.Pixbuf, get_height=lambda: DEFAULT_SIZE)
        with patch_load_icon(side_effect=[Exception, m_pixbuf]) as m_load_icon, patch_log() as m_log:
            m_load_icon.return_value.scale_simple.return_value = m_pixbuf
            pixbuf = get_from_name()
        self.assertEqual(
            m_load_icon.call_args_list,
            [mock.call("gtk-execute", 24, 0), mock.call("gtk-execute", 24, 0)]
        )
        self.assertEqual(m_log.warning.call_count, 1)
        self.assertEqual(m_log.error.call_count, 0)
        self.assertEqual(pixbuf, m_pixbuf)
        # more than one exception would fallback to random alter icon loading
        with patch_load_icon(side_effect=[Exception, Exception, m_pixbuf]) as m_load_icon, patch_log() as m_log:
            m_load_icon.return_value.scale_simple.return_value = m_pixbuf
            pixbuf = get_from_name()
        self.assertEqual(
            m_load_icon.call_args_list,
            [mock.call("gtk-execute", 24, 0), mock.call("gtk-execute", 24, 0), mock.call(mock.ANY, 24, 0)]
        )
        self.assertEqual(m_log.warning.call_count, 1)
        self.assertEqual(m_log.error.call_count, 1)
        self.assertEqual(pixbuf, m_pixbuf)

    def test_get_from_list(self):
        """Only the last working pixbuf loaded should be returned."""
        m_pixbuf = mock.Mock(spec=GdkPixbuf.Pixbuf, get_height=lambda: DEFAULT_SIZE)
        names = ("icon-name1", "icon-name2")
        size = 1234
        with patch_load_icon() as m_load_icon, patch_log() as m_log, patch_get_from_name() as m_get_from_name:
            m_load_icon.side_effect = [None, m_pixbuf]
            pixbuf = get_from_list(names, size)
        self.assertEqual(
            m_load_icon.call_args_list, [
                mock.call("icon-name1", size, Gtk.IconLookupFlags.USE_BUILTIN),
                mock.call("icon-name2", size, Gtk.IconLookupFlags.USE_BUILTIN)
            ]
        )
        self.assertEqual(m_log.method_calls, [])
        self.assertEqual(m_get_from_name.call_args_list, [])
        self.assertEqual(pixbuf, m_pixbuf)

    def test_get_from_list_exception(self):
        """On exception the next pixbuf is returned."""
        m_pixbuf = mock.Mock(spec=GdkPixbuf.Pixbuf, get_height=lambda: DEFAULT_SIZE)
        names = ("icon-name1", "icon-name2")
        size = 1234
        with patch_load_icon() as m_load_icon, patch_log() as m_log, patch_get_from_name() as m_get_from_name:
            m_load_icon.side_effect = [Exception, m_pixbuf]
            pixbuf = get_from_list(names, size)
        self.assertEqual(
            m_load_icon.call_args_list, [
                mock.call("icon-name1", size, Gtk.IconLookupFlags.USE_BUILTIN),
                mock.call("icon-name2", size, Gtk.IconLookupFlags.USE_BUILTIN)
            ]
        )
        self.assertEqual(
            m_log.method_calls,
            [mock.call.warning('get_from_list for icon-name1 failed, try next')]
        )
        self.assertEqual(m_get_from_name.call_args_list, [])
        self.assertEqual(pixbuf, m_pixbuf)

    def test_get_from_list_fallback(self):
        """Should fallback on `get_from_name()` if no icons are found."""
        m_pixbuf = mock.Mock(spec=GdkPixbuf.Pixbuf, get_height=lambda: DEFAULT_SIZE)
        names = ("icon-name1",)
        size = 1234
        with patch_load_icon() as m_load_icon, patch_log() as m_log, patch_get_from_name() as m_get_from_name:
            m_load_icon.side_effect = [Exception]
            m_get_from_name.return_value = m_pixbuf
            pixbuf = get_from_list(names, size)
        self.assertEqual(
            m_load_icon.call_args_list, [
                mock.call("icon-name1", size, Gtk.IconLookupFlags.USE_BUILTIN),
            ]
        )
        self.assertEqual(
            m_log.method_calls,
            [mock.call.warning('get_from_list for icon-name1 failed, try next')]
        )
        self.assertEqual(
            m_get_from_name.call_args_list,
            [mock.call('application-x-executable', size=size)]
        )
        self.assertEqual(pixbuf, m_pixbuf)

    def test_get_from_mime_type(self):
        """By defaults returns the pixbuf using `get_from_list()`."""
        m_pixbuf = mock.Mock(spec=GdkPixbuf.Pixbuf)
        mime = "application/vnd.debian.binary-package"
        size = 1234
        with patch_log() as m_log, patch_get_from_list() as m_get_from_list, patch_get_from_name() as m_get_from_name:
            m_get_from_list.return_value = m_pixbuf
            pixbuf = get_from_mime_type(mime, size)
        self.assertEqual(
            m_get_from_list.call_args_list, [
                mock.call(["application-vnd.debian.binary-package", "package-x-generic"], size=size),
            ]
        )
        self.assertEqual(m_log.method_calls, [])
        self.assertEqual(m_get_from_name.call_args_list, [])
        self.assertEqual(pixbuf, m_pixbuf)

    def test_get_from_mime_type_fallback(self):
        """Should fallback to `get_from_name()` on exception."""
        m_pixbuf = mock.Mock(spec=GdkPixbuf.Pixbuf)
        mime = "application/vnd.debian.binary-package"
        size = 1234
        with patch_log() as m_log, patch_get_from_list() as m_get_from_list, patch_get_from_name() as m_get_from_name:
            m_get_from_list.side_effect = [Exception]
            m_get_from_name.return_value = m_pixbuf
            pixbuf = get_from_mime_type(mime, size)
        self.assertEqual(
            m_get_from_list.call_args_list, [
                mock.call(["application-vnd.debian.binary-package", "package-x-generic"], size=size),
            ]
        )
        self.assertEqual(
            m_log.method_calls, [mock.call.error('get_from_mime_type failed: ')])
        self.assertEqual(m_get_from_name.call_args_list, [mock.call(size=size)])
        self.assertEqual(pixbuf, m_pixbuf)

    def test_get_from_file(self):
        """By defaults returns the pixbuf using `new_from_file_at_size()`."""
        m_pixbuf = mock.Mock(spec=GdkPixbuf.Pixbuf)
        file_path = "/path/to/file"
        size = 1234
        with patch_log() as m_log, patch_get_from_name() as m_get_from_name, \
                patch_new_from_file_at_size() as m_new_from_file_at_size:
            m_new_from_file_at_size.return_value = m_pixbuf
            pixbuf = get_from_file(file_path, size)
        self.assertEqual(m_get_from_name.call_args_list, [])
        self.assertEqual(m_log.method_calls, [])
        self.assertEqual(
            m_new_from_file_at_size.call_args_list, [mock.call(file_path, size, size)])
        self.assertEqual(m_get_from_name.call_args_list, [])
        self.assertEqual(pixbuf, m_pixbuf)

    def test_get_from_file_fallback(self):
        """Should fallback to `get_from_name()` on exception."""
        m_pixbuf = mock.Mock(spec=GdkPixbuf.Pixbuf)
        file_path = "/path/to/file"
        size = 1234
        with patch_log() as m_log, patch_get_from_name() as m_get_from_name, \
                patch_new_from_file_at_size() as m_new_from_file_at_size:
            m_new_from_file_at_size.side_effect = [Exception]
            m_get_from_name.return_value = m_pixbuf
            pixbuf = get_from_file(file_path, size)
        self.assertEqual(m_get_from_name.call_args_list, [mock.call(only_path=False, size=1234)])
        self.assertEqual(m_log.method_calls, [mock.call.error('get_from_file failed: ')])
        self.assertEqual(
            m_new_from_file_at_size.call_args_list, [mock.call(file_path, size, size)])
        self.assertEqual(m_get_from_name.call_args_list, [mock.call(only_path=False, size=1234)])
        self.assertEqual(
            m_log.method_calls, [mock.call.error('get_from_file failed: ')])
        self.assertEqual(pixbuf, m_pixbuf)
