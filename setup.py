import glob
from setuptools import setup, find_packages
from ubuntucleaner import __version__

setup(
    name='ubuntu-cleaner',
    version=__version__,
    description='Keep your ubuntu system clean has never been so easy!',
    author='Gerard Puig',
    author_email='gerardpuigdev@gmail.com',
    scripts=['ubuntu-cleaner'],
    packages=find_packages(exclude=['tests']),
    data_files=[
        ('../etc/dbus-1/system.d/', ['data/ubuntu-cleaner-daemon.conf']),
        ('share/dbus-1/system-services', ['data/com.ubuntu_cleaner.daemon.service']),
        ('share/polkit-1/actions/', ['data/com.ubuntu-cleaner.daemon.policy']),
        ('share/applications/', ['data/ubuntu-cleaner.desktop']),
        ('share/ubuntu-cleaner/ui/', glob.glob('data/ui/*.xml')),
        ('share/icons/hicolor/128x128/apps/', ['data/icons/128x128/apps/ubuntu-cleaner.png']),
        ('share/icons/hicolor/64x64/apps/', ['data/icons/64x64/apps/ubuntu-cleaner.png']),
        ('share/icons/hicolor/48x48/apps/', ['data/icons/48x48/apps/ubuntu-cleaner.png']),
        ('share/icons/hicolor/32x32/apps/', ['data/icons/32x32/apps/ubuntu-cleaner.png']),
        ('share/ubuntu-cleaner/', ['data/ubuntu-cleaner-daemon']),
    ],
    install_requires=[
        'lxml',
        'dbus',
        'defer',
        'apt',
        'python-aptdaemon',
        'python-aptdaemon.gtk3widgets'
    ],
    license='GNU GPL',
    platforms='linux',
)
