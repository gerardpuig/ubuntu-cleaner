import os
import gettext

from gi.repository import GLib

from ubuntucleaner import __version__

__all__ = (
        'APP',
        'PACKAGE',
        'VERSION',
        'DATA_DIR',
        'init_locale',
        )


def applize(package):
    return ' '.join([a.capitalize() for a in package.split('-')])

PACKAGE = 'ubuntu-cleaner'
VERSION = __version__
PKG_VERSION = VERSION
DATA_DIR = '/usr/share/ubuntu-cleaner/'
APP = applize(PACKAGE)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_ROOT = os.path.join(GLib.get_user_config_dir(), 'ubuntu-cleaner')
IS_INSTALLED = True

try:
    LANG = os.getenv('LANG').split('.')[0].lower().replace('_', '-')
except:
    LANG = 'en-us'

if not __file__.startswith('/usr'):
    datadir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    DATA_DIR = os.path.join(datadir, 'data')
    IS_INSTALLED = False


def init_locale():
    global INIT
    try:
        INIT
    except:
        gettext.install(PACKAGE, unicode=True)

        INIT = True

init_locale()
