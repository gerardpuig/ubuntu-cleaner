import logging
import os

from ubuntucleaner.janitor import JanitorPlugin
from ubuntucleaner.settings.debug import get_traceback
from ubuntucleaner.janitor import CruftObject

log = logging.getLogger('Janitor')

class DebInstallersPlugin(JanitorPlugin):
    __title__ = _('Deb Installers')
    __category__ = 'personal'

    def __init__(self):
        self.downloads_folder = os.path.expanduser("~/Downloads")
        JanitorPlugin.__init__(self)

    def get_cruft(self):
        try:
            count = 0
            size = 0
            for file in os.listdir(self.downloads_folder):
                if file.endswith(".deb"):
                    count += 1
                    file_size = os.path.getsize(
                        os.path.join(self.downloads_folder, file)
                    )
                    size += file_size
                    object = CruftObject(file, size=file_size)
                    self.emit('find_object', object, count)
            print(count)
            self.emit('scan_finished', True, count, size)
        except Exception, e:
            error = get_traceback()
            log.error(error)
            self.emit('scan_error', error)

    def clean_cruft(self, cruft_list=[], parent=None):
        for index, cruft in enumerate(cruft_list):
            try:
                log.debug('Cleaning...%s' % cruft.get_name())
                os.remove(os.path.join(self.downloads_folder, cruft.name))
                self.emit('object_cleaned', cruft, index + 1)
            except Exception, e:
                log.error(run_traceback(e))
                self.emit('clean_error', cruft.get_name())
                break

        self.emit('all_cleaned', True)
