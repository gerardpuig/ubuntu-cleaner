VIRTUAL_ENV ?= venv
PIP=$(VIRTUAL_ENV)/bin/pip
PYTHON=$(VIRTUAL_ENV)/bin/python
PYTHON_MAJOR_VERSION=2
PYTHON_MINOR_VERSION=7
SYSTEM_DEPENDENCIES= \
    gir1.2-notify-0.7 \
    libpython$(PYTHON_VERSION)-dev \
    python$(PYTHON_VERSION) \
    python$(PYTHON_VERSION)-dev \
    python-aptdaemon \
    python-aptdaemon.gtk3widgets \
    python-gi \
    virtualenv
PYTHON_VERSION=$(PYTHON_MAJOR_VERSION).$(PYTHON_MINOR_VERSION)
PYTHON_MAJOR_MINOR=$(PYTHON_MAJOR_VERSION)$(PYTHON_MINOR_VERSION)
PYTHON_WITH_VERSION=python$(PYTHON_VERSION)
DOCKER_IMAGE=gerardpuig/ubuntu-cleaner
DOCKER_VOLUME=/tmp/.X11-unix:/tmp/.X11-unix

all: virtualenv

system_dependencies:
	apt install --yes --no-install-recommends $(SYSTEM_DEPENDENCIES)

$(VIRTUAL_ENV):
	virtualenv --python=$(PYTHON_WITH_VERSION) --system-site-packages $(VIRTUAL_ENV)
	$(PIP) install lxml

virtualenv: $(VIRTUAL_ENV)

deb:
	python setup.py --command-packages=stdeb.command sdist_dsc --package ubuntu-cleaner bdist_deb

clean:
	@rm -rf deb_dist dist ubuntu_cleaner.egg-info
	@rm -f ubuntu-cleaner*.tar.gz

test: virtualenv
	$(PYTHON) -m unittest discover tests

run: virtualenv
	$(PYTHON) ubuntu-cleaner

docker/build:
	docker build --tag=$(DOCKER_IMAGE) .

docker/make/%:
	docker run -e DISPLAY -v $(DOCKER_VOLUME) --rm $(DOCKER_IMAGE) make $*

docker/shell:
	docker run -e DISPLAY -v $(DOCKER_VOLUME) -it --rm $(DOCKER_IMAGE)
