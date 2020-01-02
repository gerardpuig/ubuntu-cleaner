import mock
import unittest

from ubuntucleaner.main import UbuntuCleanerWindow


class TestUbuntuCleanerWindow(unittest.TestCase):
    def setUp(self):
        self.window = UbuntuCleanerWindow()

    def tearDown(self):
        del self.window

    def test_app(self):
        self.assertEqual(self.window.feature_dict, {'janitor': 0})
        self.assertIsNotNone(self.window.aboutdialog)

    def test_on_about_button_clicked(self):
        with mock.patch("ubuntucleaner.main.Gtk.AboutDialog.run") as m_run:
            self.window.about_button.clicked()
        self.assertEqual(m_run.call_args_list, [mock.call()])

    def test_on_mainwindow_destroy(self):
        with mock.patch("ubuntucleaner.main.Gtk.main_quit") as m_main_quit, \
                mock.patch("ubuntucleaner.main.exit") as m_exit:
            self.window.mainwindow.destroy()
        self.assertEqual(m_main_quit.call_args_list, [mock.call()])
        self.assertEqual(m_exit.call_args_list, [mock.call()])
