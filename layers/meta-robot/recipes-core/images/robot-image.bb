SUMMARY = "Robot image."
LICENSE = "MIT & GPL-2.0-or-later"

GLIBC_GENERATE_LOCALES = "fr_FR.UTF-8"
IMAGE_LINGUAS = "fr-fr"

ENABLE_UART="1"
#RPI_USE_U_BOOT = "1"


IMAGE_FSTYPES = "ext4 ext3 wic"
IMAGE_OVERHEAD_FACTOR = "1.1"

#require recipes-core/images/core-image-minimal.bb

IMAGE_ROOTFS_SIZE ?= "8192"
#IMAGE_ROOTFS_EXTRA_SPACE:append = "${@bb.utils.contains("DISTRO_FEATURES", "systemd", " + 4096", "", d)}"

#IMAGE_INSTALL = "packagegroup-core-boot ${CORE_IMAGE_EXTRA_INSTALL}"
#IMAGE_INSTALL:append = " wpa-supplicant"
#IMAGE_INSTALL:append = " net-tools"
#IMAGE_INSTALL:append = " openssh-sshd"
#IMAGE_INSTALL:append = " networkmanager"
#IMAGE_INSTALL:append = " dropbear"
#IMAGE_INSTALL:append = " glibc-utils"
#IMAGE_INSTALL:append = " linux-firmware iw networkmanager wpa-supplicant"
#IMAGE_INSTALL:append = " vim valgrind"

#IMAGE_INSTALL:append = " python3"
#IMAGE_INSTALL:append = " python3-modules"


#IMAGE_FEATURES += "tools-debug"
#IMAGE_FEATURES += "tools-profile"
#IMAGE_FEATURES += "tools-sdk"
#IMAGE_FEATURES += "ssh-server-openssh"
#IMAGE_FEATURES += "allow-root-login"
#IMAGE_FEATURES += "x11-base"
#IMAGE_FEATURES += "bash-completion-pkgs"


IMAGE_FEATURES:remove = "splash"
IMAGE_FEATURES:remove = "package-management"
IMAGE_FEATURES:append = " x11-base"
IMAGE_FEATURES:append = " allow-root-login"
IMAGE_FEATURES:append = " allow-empty-password"
IMAGE_FEATURES:append = " empty-root-password"
IMAGE_FEATURES:append = " post-install-logging"
IMAGE_FEATURES:append = " ssh-server-dropbear"

IMAGE_INSTALL:append = " os-release"
IMAGE_INSTALL:append = " procps"
IMAGE_INSTALL:append = " file"
IMAGE_INSTALL:append = " zile"
IMAGE_INSTALL:append = " cpufrequtils"
IMAGE_INSTALL:append = " msmtp"

TOOLCHAIN_HOST_TASK += "nativesdk-cmake"

inherit core-image features_check extrausers
# user : robot ; mdp : robot
EXTRA_USERS_PARAMS += "useradd -p '\$5\$AOGM1KFw2Detl3xH\$40yCsKtsfhfmgVcLwVbt.mkY2zvZy0frUhIKas9L8b1' robot;"
# user : root ; mdp : admin
EXTRA_USERS_PARAMS += "usermod -p '\$5\$DWOEERq5VEhODWxL\$.6QFc1PwhB/KphCmAhd4WlNZX0jvwgV82dZUNmdMe89' root;"
