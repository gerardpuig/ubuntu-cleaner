from ubuntucleaner.janitor import JanitorCachePlugin


class EdgeCachePlugin(JanitorCachePlugin):
    __title__ = _('Edge Cache')
    __category__ = 'application'

    root_path = '~/.cache/microsoft-edge/Default'


class EdgeDevCachePlugin(JanitorCachePlugin):
    __title__ = _('Edge-dev Cache')
    __category__ = 'application'

    root_path = '~/.cache/microsoft-edge-dev/Default'
