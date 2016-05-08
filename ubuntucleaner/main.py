import logging

from gi.repository import Gtk

from ubuntucleaner.gui import GuiBuilder
from ubuntucleaner.settings.constants import VERSION
from ubuntucleaner.janitor import JanitorPage
from ubuntutweak.utils import icon

log = logging.getLogger('app')


class UbuntuCleanerWindow(GuiBuilder):
    feature_dict = {}

    def __init__(self):
        GuiBuilder.__init__(self, file_name='mainwindow.xml')
        self.load_janitor()
        self.mainwindow.show()

    def on_mainwindow_destroy(self, widget=None):
        Gtk.main_quit()
        exit()

    def on_about_button_clicked(self, widget):
        self.aboutdialog.set_version(VERSION)
        self.aboutdialog.set_transient_for(self.mainwindow)
        self.aboutdialog.run()
        self.aboutdialog.hide()

    def load_janitor(self):
        janitor_page = JanitorPage()
        self.feature_dict['janitor'] = self.notebook.append_page(janitor_page, Gtk.Label('janitor'))
        self.module_image.set_from_pixbuf(icon.get_from_name('computerjanitor', size=48))
        self.title_label.set_markup('<b><big>%s</big></b>' % _('Computer Janitor'))
        self.description_label.set_text(_("Clean up a system so it's more like a freshly installed one"))