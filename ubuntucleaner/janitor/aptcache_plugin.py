import logging

from ubuntucleaner.janitor import JanitorCachePlugin

log = logging.getLogger('aptcache_plugin')


class AptCachePlugin(JanitorCachePlugin):
    __title__ = _('Apt Cache')
    __category__ = 'system'

    root_path = '/var/cache/apt/archives/'
    pattern = '*.deb'
