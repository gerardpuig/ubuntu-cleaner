#!/usr/bin/python

import os
import logging
import dbus
import dbus.service
import dbus.mainloop.glib

from ubuntucleaner.daemon import PolicyKitService, PK_ACTION_CLEAN

log = logging.getLogger('DaemonService')

INTERFACE = "com.ubuntu_cleaner.daemon"
PATH = "/com/ubuntu_cleaner/daemon"


class DaemonService(PolicyKitService):

    def __init__(self, bus, mainloop):
        bus_name = dbus.service.BusName(INTERFACE, bus=bus)
        PolicyKitService.__init__(self, bus_name, PATH)
        self.mainloop = mainloop

    @dbus.service.method(INTERFACE,
                         in_signature='s', out_signature='b',
                         sender_keyword='sender')
    def delete_apt_cache_file(self, file_name, sender=None):
        self._check_permission(sender, PK_ACTION_CLEAN)

        full_path = os.path.join('/var/cache/apt/archives/', file_name)
        if os.path.exists(full_path):
            os.remove(full_path)

        return not os.path.exists(full_path)

    @dbus.service.method(INTERFACE,
                         in_signature='', out_signature='')
    def exit(self):
        self.mainloop.quit()
