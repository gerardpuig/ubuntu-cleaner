import unittest
import mock

from gi.repository import GdkPixbuf
from ubuntucleaner.utils.icon import get_from_name, DEFAULT_SIZE


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
