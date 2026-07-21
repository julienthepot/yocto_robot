# Base this image on core-image-base
include recipes-core/images/core-image-base.bb

COMPATIBLE_MACHINE = "^rpi$"

# Type de dispositif (identifiant du type de matériel)
# MENDER_DEVICE_TYPE = "raspberrypi0-w"

IMAGE_FEATURES:remove = "splash"
IMAGE_FEATURES:remove = "package-management"
IMAGE_FEATURES:append = " allow-root-login"
IMAGE_FEATURES:append = " allow-empty-password"
IMAGE_FEATURES:append = " empty-root-password"
IMAGE_FEATURES:append = " post-install-logging"
IMAGE_FEATURES:append = " ssh-server-openssh"
IMAGE_FEATURES:append = " debug-tweaks "

IMAGE_INSTALL:append = " python3"
IMAGE_INSTALL:append = " os-release"
IMAGE_INSTALL:append = " procps"
IMAGE_INSTALL:append = " file"
IMAGE_INSTALL:append = " zile"
IMAGE_INSTALL:append = " cpufrequtils"
IMAGE_INSTALL:append = " config-wifi"
IMAGE_INSTALL:append = " curl"
IMAGE_INSTALL:append = " systemd-analyze"
IMAGE_INSTALL:append = " mpu-9250-6500"
IMAGE_INSTALL:append = " zlib"
IMAGE_INSTALL:append = " libuv"
IMAGE_INSTALL:append = " syslog-ng logrotate"

DISTRO_FEATURES:append = " wifi"
IMAGE_INSTALL:append = " linux-firmware-rpidistro-bcm43430"

# mkpasswd -m sha256crypt <your-password>
# password: ppp
PASSWD = "\$5\$2qQtEpyiwk33Lj5/\$KK0mV7X4Mzt15EAo56iymdLUtL9Bbv0HWe8hpUZdhm1"
EXTRA_USERS_PARAMS = "\
    usermod -p '${PASSWD}' root; \
"

REQUIRED_DISTRO_FEATURES = "cpufrequtils"
