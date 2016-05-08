import os
import platform

from ubuntucleaner.settings.constants import APP, PKG_VERSION


def get_distro():
    return ' '.join(platform.dist())


def get_codename():
    return os.popen('lsb_release -cs').read().strip()


def get_desktop():
    '''
    ubuntu
    ubuntu-2d
    gnome-classic
    gnome-shell
    '''
    return os.getenv('DESKTOP_SESSION')


def get_app():
    '''Ubuntu Cleaner 0.5.x'''
    return " ".join([APP, PKG_VERSION])


DISTRO = get_distro()
CODENAME = get_codename()
DESKTOP = get_desktop()
APP = get_app()


if __name__ == '__main__':
    print 'DISTRO: ', DISTRO
    print 'CODENAME: ', CODENAME
    print 'DESKTOP: ', DESKTOP
    print 'APP: ', APP
