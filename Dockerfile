# Docker image for installing dependencies on Linux and running tests.
# Build with:
# docker build --tag=gerardpuig/ubuntu-cleaner --file=dockerfiles/Dockerfile-linux .
# Run with:
# docker run -it --rm gerardpuig/ubuntu-cleaner make test
# Or for interactive shell:
# docker run -it --rm gerardpuig/ubuntu-cleaner
# For running UI:
# xhost +"local:docker@"
# docker run -e DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --it -rm gerardpuig/ubuntu-cleaner ubuntu-cleaner
FROM ubuntu:18.04

ENV USER="user"
ENV HOME_DIR="/home/${USER}"
ENV WORK_DIR="${HOME_DIR}/app"

# configure locale
RUN apt update -qq > /dev/null && apt install -qq --yes --no-install-recommends \
    locales \
    && locale-gen en_US.UTF-8 \
    && rm -rf /var/lib/apt/lists/*
ENV LANG="en_US.UTF-8" \
    LANGUAGE="en_US.UTF-8" \
    LC_ALL="en_US.UTF-8"

# install minimal system dependencies
RUN apt update -qq > /dev/null && apt install -qq --yes --no-install-recommends \
    make \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# prepare non root env, with sudo access and no password
RUN useradd --create-home --home-dir ${HOME_DIR} --shell /bin/bash ${USER} \
    && usermod -append --groups sudo ${USER} \
    && echo "%sudo ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers \
    && mkdir ${WORK_DIR} \
    && chown ${USER}:${USER} -R ${WORK_DIR}

USER ${USER}
WORKDIR ${WORK_DIR}

# install app dependencies
COPY Makefile requirements.txt setup.py ${WORK_DIR}/
RUN sudo apt update -qq > /dev/null \
    && sudo make system_dependencies \
    && make virtualenv \
    && sudo rm ${WORK_DIR}/Makefile ${WORK_DIR}/requirements.txt ${WORK_DIR}/setup.py \
    && sudo rm -rf /var/lib/apt/lists/*

COPY . ${WORK_DIR}
