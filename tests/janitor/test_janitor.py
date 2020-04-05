import unittest

from gi.repository import Gtk

import mock
from ubuntucleaner.janitor import JanitorPage


class TestJanitorPage(unittest.TestCase):
    def setUp(self):
        self.janitor_page = JanitorPage()

    def test_on_clean_button_clicked(self):
        with mock.patch(
            "ubuntucleaner.janitor.JanitorPage.set_busy"
        ) as m_set_busy, mock.patch(
            "ubuntucleaner.janitor.JanitorPage.do_real_clean_task"
        ) as m_do_real_clean_task:
            self.janitor_page.on_clean_button_clicked(widget=Gtk.Label("test"))

        m_set_busy.assert_called_once_with()
        m_do_real_clean_task.assert_called_once_with()
