import logging

from ubuntucleaner.janitor import JanitorCachePlugin
from ubuntucleaner.daemon.dbusproxy import proxy

log = logging.getLogger('aptcache_plugin')


class AptCachePlugin(JanitorCachePlugin):
    __title__ = _('Apt Cache')
    __category__ = 'system'

    root_path = '/var/cache/apt/archives/'
    pattern = '*.deb'

    def clean_cruft(self, cruft_list=[], parent=None):
        for index, cruft in enumerate(cruft_list):
            if cruft:
                log.debug('Cleaning...%s' % cruft.get_name())
                result = proxy.delete_apt_cache_file(cruft.get_name())

                if bool(result) == False:
                    self.emit('clean_error', cruft.get_name())
                    break
                else:
                    self.emit('object_cleaned', cruft, index + 1)

        self.emit('all_cleaned', True)
