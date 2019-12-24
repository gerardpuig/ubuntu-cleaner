import unittest
import mock

from ubuntucleaner.utils.system import get_distro, get_codename, get_desktop


def patch_load_icon(side_effect=None):
    return mock.patch(
        "ubuntucleaner.utils.icon.Gtk.IconTheme.load_icon",
        side_effect=side_effect)


def patch_log():
    return mock.patch("ubuntucleaner.utils.icon.log")


def patch_get_from_name():
    return mock.patch("ubuntucleaner.utils.icon.get_from_name")


class TestSystemModule(unittest.TestCase):

    def test_get_distro(self):
        with mock.patch("ubuntucleaner.utils.system.platform.dist") as m_dist:
            m_dist.return_value = ('Ubuntu', '18.04', 'bionic')
            distro = get_distro()
        self.assertEqual(
            m_dist.call_args_list, [mock.call()]
        )
        self.assertEqual(distro, 'Ubuntu 18.04 bionic')

    def test_get_codename(self):
        """The codename is retrieved executing a `lsb_release` via `popen()`."""
        with mock.patch("ubuntucleaner.utils.system.platform.os.popen") as m_popen:
            m_popen.return_value.read.return_value = 'bionic\n'
            codename = get_codename()
        self.assertEqual(
            m_popen.call_args_list, [mock.call('lsb_release -cs')]
        )
        self.assertEqual(codename, 'bionic')

    def test_get_desktop(self):
        """Desktop is retrieved from environment variable."""
        environ = {"DESKTOP_SESSION": "ubuntu"}
        with mock.patch.dict("ubuntucleaner.utils.system.platform.os.environ", environ):
            desktop = get_desktop()
        self.assertEqual(
            desktop, environ["DESKTOP_SESSION"]
        )
