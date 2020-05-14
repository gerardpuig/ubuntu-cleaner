from ubuntucleaner.janitor import JanitorCachePlugin


class ChromeCachePlugin(JanitorCachePlugin):
    __title__ = _('Chrome Cache')
    __category__ = 'application'

    root_path = '~/.cache/google-chrome/Default'


class ChromiumCachePlugin(JanitorCachePlugin):
    __title__ = _('Chromium Cache')
    __category__ = 'application'

    root_path = '~/.cache/chromium/Default'


class ChromiumSnapCachePlugin(JanitorCachePlugin):
    __title__ = _('Chromium Cache')
    __category__ = 'application'

    root_path = '~/snap/chromium/common/.cache/chromium/Default'
