import os
import logging

from ubuntucleaner.janitor import JanitorPlugin, PackageObject
from ubuntucleaner.utils import icon


log = logging.getLogger('PackageConfigsPlugin')


class PackageConfigObject(PackageObject):
    def __init__(self, name):
        self.name = name

    def get_icon(self):
        return icon.get_from_name('text-plain')

    def get_size_display(self):
        return ''

    def get_size(self):
        return 0


class PackageConfigsPlugin(JanitorPlugin):
    __title__ = _('Package Configs')
    __category__ = 'system'

    def get_cruft(self):
        count = 0

        for line in os.popen('dpkg -l'):
            try:
                temp_list = line.split()
                status, pkg = temp_list[0], temp_list[1]
                if status == 'rc':
                    des = temp_list[3:]
                    count += 1
                    self.emit('find_object',
                              PackageConfigObject(pkg),
                              count)
            except:
                pass

        self.emit('scan_finished', True, count, 0)

    def get_summary(self, count):
        if count:
            return '[%d] %s' % (count, self.__title__)
        else:
            return _('Packages Configs (No package config to be removed)')
