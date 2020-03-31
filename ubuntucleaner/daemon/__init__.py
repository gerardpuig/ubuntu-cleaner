import dbus
import dbus.service

PK_ACTION_CLEAN = 'com.ubuntu-cleaner.daemon.clean'


class AccessDeniedException(dbus.DBusException):
    '''This exception is raised when some operation is not permitted.'''

    _dbus_error_name = 'com.ubuntu_cleaner.daemon.AccessDeniedException'


class PolicyKitService(dbus.service.Object):
    '''A D-BUS service that uses PolicyKit for authorization.'''

    def _check_permission(self, sender, action):
        '''
        Verifies if the specified action is permitted, and raises
        an AccessDeniedException if not.

        The caller should use ObtainAuthorization() to get permission.
        '''

        try:
            if sender:
                kit = dbus.SystemBus().get_object('org.freedesktop.PolicyKit1', '/org/freedesktop/PolicyKit1/Authority')
                kit = dbus.Interface(kit, 'org.freedesktop.PolicyKit1.Authority')

                (granted, _, details) = kit.CheckAuthorization(
                                ('system-bus-name', {'name': sender}),
                                action, {}, dbus.UInt32(1), '', timeout=600)

                if not granted:
                    raise AccessDeniedException('Session not authorized by PolicyKit')

        except AccessDeniedException:
            raise

        except dbus.DBusException as ex:
            raise AccessDeniedException(ex.message)
