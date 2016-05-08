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
        ('share/applications/', ['data/ubuntu-cleaner.desktop']),
        ('share/ubuntu-cleaner/ui/', glob.glob('data/ui/*.xml'))
    ],
    license='GNU GPL',
    platforms='linux',
)
