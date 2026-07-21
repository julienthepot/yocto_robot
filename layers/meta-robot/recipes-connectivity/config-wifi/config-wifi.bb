SUMMARY = "wireless configuration"
DESCRIPTION = "wireless configuration for FR reg domain"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

inherit systemd

RDEPENDS:${PN} = "\
  wireless-regdb-static \
  iw \
  bash \
  connman \
  connman-client \
"

SYSTEMD_SERVICE:${PN} = "config-wifi.service unblock_wifi.service"
SYSTEMD_AUTO_ENABLE:${PN} = "enable"

RPI_KERNEL_DEVICETREE_OVERLAYS:remove = " \
    overlays/disable-bt.dtbo \
    overlays/disable-wifi.dtbo \
"

SRC_URI = "file://config-wifi.service \
           file://config-wifi.sh \
           file://config-wifi.env \
           file://unblock_wifi.service \
"

do_install () {
  install -d ${D}${sysconfdir}/default
  echo 'COUNTRY=FR' > ${D}${sysconfdir}/default/regulatory
  
  # Automatically load WiFi module at boot
  install -d ${D}${sysconfdir}/modules-load.d
  echo 'brcmfmac' > ${D}${sysconfdir}/modules-load.d/wifi.conf

  # Install script
  install -D -m 0755 ${WORKDIR}/config-wifi.sh ${D}${bindir}/config-wifi.sh

  # Install WiFi runtime configuration template (no secrets)
  install -D -m 0644 ${WORKDIR}/config-wifi.env ${D}${sysconfdir}/default/config-wifi
  
  # Install systemd service
  install -D -m 0644 ${WORKDIR}/config-wifi.service ${D}${systemd_system_unitdir}/config-wifi.service
  install -D -m 0644 ${WORKDIR}/unblock_wifi.service ${D}${systemd_system_unitdir}/unblock_wifi.service
}

FILES:${PN} += "${sysconfdir}/default/* \
                ${sysconfdir}/modules-load.d/* \
                ${bindir}/* \
                ${systemd_system_unitdir}/* \
"
