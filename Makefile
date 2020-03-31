VIRTUAL_ENV ?= venv
PIP=$(VIRTUAL_ENV)/bin/pip
PYTHON=$(VIRTUAL_ENV)/bin/python
PYTHON_MAJOR_VERSION=3
PYTHON_MINOR_VERSION=6
COVERALLS=$(VIRTUAL_ENV)/bin/coveralls
COVERAGE=$(VIRTUAL_ENV)/bin/coverage
SYSTEM_DEPENDENCIES= \
    gir1.2-notify-0.7 \
    git \
    libpython$(PYTHON_VERSION)-dev \
    python$(PYTHON_VERSION) \
    python$(PYTHON_VERSION)-dev \
    python3-aptdaemon \
    python3-aptdaemon.gtk3widgets \
    python3-gi \
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
	$(PIP) install -r requirements.txt

virtualenv: $(VIRTUAL_ENV)

deb:
	$(PYTHON) setup.py --command-packages=stdeb.command sdist_dsc --package ubuntu-cleaner bdist_deb

clean:
	@rm -rf deb_dist dist ubuntu_cleaner.egg-info
	@rm -f ubuntu-cleaner*.tar.gz

test: virtualenv
	$(COVERAGE) run --source=ubuntucleaner -m unittest discover tests
	$(COVERAGE) report
	@if [ -n "$$CI" ]; then $(COVERALLS); fi \

run: virtualenv
	$(PYTHON) ubuntu-cleaner

docker/build:
	docker build --tag=$(DOCKER_IMAGE) .

docker/make/%:
	docker run --env-file docker.env -v $(DOCKER_VOLUME) --rm $(DOCKER_IMAGE) make $*

docker/shell:
	docker run --env-file docker.env -v $(DOCKER_VOLUME) -it --rm $(DOCKER_IMAGE)

.ONESHELL:
launchpad: deb
	cd deb_dist
	debsign `ls *source.changes`
	dput ppa:gerardpuig/ppa `ls *source.changes`
