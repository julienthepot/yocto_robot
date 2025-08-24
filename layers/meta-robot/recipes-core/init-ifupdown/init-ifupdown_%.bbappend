# Prepend the init-ifupdown script to the initial config 
FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

IMAGE_INSTALL:append = " resolvconf"