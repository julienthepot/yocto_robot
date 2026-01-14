FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

do_install:append() {
    # Create /data/connman directory
    install -d ${D}/data/connman
}
