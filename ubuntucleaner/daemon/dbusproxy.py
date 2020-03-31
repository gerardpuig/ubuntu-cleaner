import dbus
import logging

log = logging.getLogger("DbusProxy")


class DbusProxy:
    INTERFACE = "com.ubuntu_cleaner.daemon"
    PATH = "/com/ubuntu_cleaner/daemon"

    try:
        bus = dbus.SystemBus()
        object = bus.get_object(INTERFACE, PATH)
    except Exception as e:
        log.error(e)
        object = None

    def __getattr__(self, name):
        try:
            return self.object.get_dbus_method(name, dbus_interface=self.INTERFACE)
        except Exception as e:
            log.error(e)

    def get_object(self):
        return self.object

proxy = DbusProxy()
