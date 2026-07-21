FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

SRC_URI:append := " file://syslog-ng.conf"

do_install:append() {
    install -m 644 ${WORKDIR}/syslog-ng.conf ${D}${sysconfdir}/${BPN}/${BPN}.conf
}
