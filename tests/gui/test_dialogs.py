import mock
import unittest
from gi.repository import Gtk

from ubuntucleaner.gui.dialogs import (
    BaseDialog, ErrorDialog, InfoDialog, WarningDialog, QuestionDialog)


class TestBaseDialog(unittest.TestCase):

    def test_base(self):
        dialog = BaseDialog()
        self.assertTrue(isinstance(dialog, Gtk.Dialog))
        self.assertEqual(dialog.get_title(), '')
        self.assertEqual(dialog.get_property('text'), '')
        self.assertIsNone(dialog.get_property('secondary-text'))

    def test_title(self):
        init_params = {'title': 'title'}
        dialog = BaseDialog(**init_params)
        self.assertEqual(dialog.get_title(), '')
        self.assertEqual(dialog.get_property('text'), '<big><b>title</b></big>')
        self.assertIsNone(dialog.get_property('secondary-text'))

    def test_message(self):
        init_params = {'message': 'message'}
        dialog = BaseDialog(**init_params)
        self.assertEqual(dialog.get_title(), '')
        self.assertEqual(dialog.get_property('text'), 'message')
        self.assertIsNone(dialog.get_property('secondary-text'))

    def test_title_message(self):
        init_params = {'title': 'title', 'message': 'message'}
        dialog = BaseDialog(**init_params)
        self.assertEqual(dialog.get_title(), '')
        self.assertEqual(dialog.get_property('text'), '<big><b>title</b></big>')
        self.assertEqual(dialog.get_property('secondary-text'), 'message')

    def test_launch(self):
        dialog = BaseDialog()
        with mock.patch("ubuntucleaner.gui.dialogs.BaseDialog.run") as m_run:
            dialog.launch()
        self.assertEqual(m_run.call_args_list, [mock.call()])

    def test_error_dialog(self):
        dialog = ErrorDialog()
        self.assertTrue(isinstance(dialog, BaseDialog))

    def test_info_dialog(self):
        dialog = InfoDialog()
        self.assertTrue(isinstance(dialog, BaseDialog))

    def test_warning_dialog(self):
        dialog = WarningDialog()
        self.assertTrue(isinstance(dialog, BaseDialog))

    def test_question_dialog(self):
        dialog = QuestionDialog()
        self.assertTrue(isinstance(dialog, BaseDialog))
