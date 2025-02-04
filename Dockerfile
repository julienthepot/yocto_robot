FROM ubuntu:22.04

# package need to build an image
RUN DEBIAN_FRONTEND=noninteractive apt update && DEBIAN_FRONTEND=noninteractive apt install -y git build-essential gawk wget \
  diffstat unzip texinfo gcc chrpath socat cpio python3 python3-pip \
  python3-pexpect xz-utils debianutils iputils-ping libsdl1.2-dev xterm \
  python3-git python3-jinja2 libegl1-mesa python3-subunit \
  mesa-common-dev zstd liblz4-tool file locales libssl-dev

# package need to build the documentation
RUN DEBIAN_FRONTEND=noninteractive apt update && DEBIAN_FRONTEND=noninteractive apt install -y make inkscape texlive-latex-extra
RUN DEBIAN_FRONTEND=noninteractive pip3 install sphinx sphinx_rtd_theme pyyaml

# package need to simu an image
RUN DEBIAN_FRONTEND=noninteractive apt update && DEBIAN_FRONTEND=noninteractive apt install -y qemu

RUN locale-gen en_US.UTF-8

ARG UNAME=worker
ARG UID=1000
ARG GID=1000
RUN groupadd -g $GID -o $UNAME
RUN useradd -m -u $UID -g $GID -o -s /bin/bash $UNAME
USER $UNAME

ENV BUILD_FOLDER=/workspace/yocto_robot

WORKDIR ${BUILD_FOLDER}
