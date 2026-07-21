FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

SRC_URI:append := " file://messages.log"

do_install:append() {
    install -m 644 ${WORKDIR}/messages.log ${D}${sysconfdir}/logrotate.d/messages.log
}
