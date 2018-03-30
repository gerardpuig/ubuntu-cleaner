# Ubuntu Cleaner #

![screenshot](data/screenshot.png)

### Introduction ###
Ubuntu Cleaner is a tool that makes it easy to clean your Ubuntu system.

- Clear browser cache
- Clear APT cache
- Clear thumbnail cache
- Remove unneeded packages
- Remove old kernels

### How to build & test ###
* `make deb` generates a .deb package ready to be installed.
* `make clean` cleans all the generated files due .deb compilation.
* `make test` runs the tests.

### Setup via PPA ###
* `sudo add-apt-repository ppa:gerardpuig/ppa` adds ubuntu-cleaner ppa.
* `sudo apt update && sudo apt install ubuntu-cleaner` installs ubuntu-cleaner.

### Related websites ###
* Blog <a href="http://ubuntu-cleaner.blogspot.com">http://ubuntu-cleaner.blogspot.com</a>.
* Launchpad <a href="https://launchpad.net/~gerardpuig/+archive/ubuntu/ppa">https://launchpad.net/~gerardpuig/+archive/ubuntu/ppa</a>.
* Github <a href="https://github.com/gerardpuig/ubuntu-cleaner">https://github.com/gerardpuig/ubuntu-cleaner</a>.

### License ###
This software is released under the GNU General Public License (GPL) version 3.
