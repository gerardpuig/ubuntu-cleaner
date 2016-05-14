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
        ('share/ubuntu-cleaner/', ['data/ubuntu-cleaner-daemon']),
    ],
    license='GNU GPL',
    platforms='linux',
)