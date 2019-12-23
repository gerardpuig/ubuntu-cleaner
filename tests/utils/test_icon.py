import unittest
import mock

from gi.repository import Gtk, GdkPixbuf
from ubuntucleaner.utils.icon import get_from_name, DEFAULT_SIZE


def patch_load_icon(side_effect):
    return mock.patch(
        "ubuntucleaner.utils.icon.Gtk.IconTheme.load_icon",
        side_effect=side_effect)


def patch_log():
    return mock.patch("ubuntucleaner.utils.icon.log")


class TestIconModule(unittest.TestCase):

    def test_get_from_name(self):
        """
        Calling with no parameters should return the pixbuf object through `load_icon()`
        and default parameters.
        """
        m_pixbuf = mock.Mock(spec=GdkPixbuf.Pixbuf, get_height=lambda: DEFAULT_SIZE)
        with mock.patch("ubuntucleaner.utils.icon.Gtk.IconTheme.load_icon") as m_load_icon:
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
