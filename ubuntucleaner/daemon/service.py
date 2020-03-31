#!/usr/bin/python3

import fcntl
import logging
import os
import subprocess

import dbus
import dbus.mainloop.glib
import dbus.service
from ubuntucleaner.daemon import PK_ACTION_CLEAN, PolicyKitService

log = logging.getLogger('DaemonService')

INTERFACE = "com.ubuntu_cleaner.daemon"
PATH = "/com/ubuntu_cleaner/daemon"


class DaemonService(PolicyKitService):
    p = None

    def __init__(self, bus, mainloop):
        bus_name = dbus.service.BusName(INTERFACE, bus=bus)
        PolicyKitService.__init__(self, bus_name, PATH)
        self.mainloop = mainloop

    def _setup_non_block_io(self, io):
        outfd = io.fileno()
        file_flags = fcntl.fcntl(outfd, fcntl.F_GETFL)
        fcntl.fcntl(outfd, fcntl.F_SETFL, file_flags | os.O_NDELAY)

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
                         in_signature='s', out_signature='',
                         sender_keyword='sender')
    def clean_configs(self, pkg, sender=None):
        self._check_permission(sender, PK_ACTION_CLEAN)
        cmd = ['sudo', 'dpkg', '--purge']
        cmd.append(pkg)
        self.p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        self._setup_non_block_io(self.p.stdout)

    @dbus.service.method(INTERFACE,
                         in_signature='', out_signature='v')
    def get_cmd_pipe(self):
        if self.p:
            terminaled = self.p.poll()
            if terminaled == None:
                try:
                    return self.p.stdout.readline(), str(terminaled)
                except:
                    return '', 'None'
            else:
                strings, returncode = ''.join(self.p.stdout.readlines()), str(terminaled)
                self.p = None
                return strings, returncode
        else:
            return '', 'None'

    @dbus.service.method(INTERFACE,
                         in_signature='', out_signature='')
    def exit(self):
        self.mainloop.quit()
