import logging
import os
import glob

from ubuntucleaner.settings.debug import get_traceback, run_traceback
from ubuntucleaner.janitor import CacheObject, JanitorPlugin

log = logging.getLogger('Janitor')

class FirefoxDataPlugin(JanitorPlugin):
    __title__ = _('Firefox Browsing Data')
    __category__ = 'application'

    def __init__(self):
        self.profile_location = os.path.expanduser("~/.mozilla/firefox")
        JanitorPlugin.__init__(self)

    def get_cruft(self):
        try:
            count = 0
            size = 0
            for profile in os.listdir(self.profile_location):
                for data in ["cookies.sqlite*", "places.sqlite*", "favicons.sqlite*", "formhistory.sqlite", "sessionstore-backups/*", "webappsstore.sqlite*"]:
                    data_list = glob.glob(os.path.join(self.profile_location, profile, data))
                    if data_list:
                        for data_item in data_list:
                            count +=1
                            file_size = os.path.getsize(data_item)
                            size += file_size
                            object = CacheObject(os.path.basename(data_item), data_item, size=file_size)
                            self.emit('find_object', object, count)

            self.emit('scan_finished', True, count, size)
        except Exception, e:
            error = get_traceback()
            log.error(error)
            self.emit('scan_error', error)

    def clean_cruft(self, cruft_list=[], parent=None):
        for index, cruft in enumerate(cruft_list):
            try:
                log.debug('Cleaning...%s' % cruft.get_name())
                os.remove(cruft.path)
                self.emit('object_cleaned', cruft, index + 1)
            except Exception, e:
                log.error(run_traceback(e))
                self.emit('clean_error', cruft.get_name())
                break

        self.emit('all_cleaned', True)
