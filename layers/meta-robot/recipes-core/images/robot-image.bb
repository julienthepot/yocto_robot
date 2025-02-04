SUMMARY = "Robot image."
LICENSE = "MIT & GPL-2.0-or-later"

inherit core-image
inherit ros_distro_${ROS_DISTRO}
inherit ${ROS_DISTRO_TYPE}_image

ENABLE_UART="1"

IMAGE_FEATURES += "tools-debug"
IMAGE_FEATURES += "tools-profile"
IMAGE_FEATURES += "tools-sdk"
IMAGE_FEATURES += "ssh-server-openssh"
#IMAGE_FEATURES += "x11"
IMAGE_FEATURES += "bash-completion-pkgs"

IMAGE_INSTALL = "packagegroup-core-boot ${CORE_IMAGE_EXTRA_INSTALL}"
IMAGE_INSTALL:append = " vim valgrind"
IMAGE_INSTALL:append = " can-utils"

IMAGE_INSTALL:append = " python3"
IMAGE_INSTALL:append = " python3-modules"

IMAGE_INSTALL:append = " opencv"

IMAGE_INSTALL:append:ros2-distro = " ros-core rclcpp-dev std-msgs-dev"
IMAGE_INSTALL:append:ros2-distro = " usb-cam turtlesim demos"

# Configuration reseau
IMAGE_INSTALL:append = " resolvconf"

TOOLCHAIN_HOST_TASK += "nativesdk-cmake"

# Add user 
INHERIT += "extrausers"

# user : robot ; mdp : robot
EXTRA_USERS_PARAMS += "usedadd -p '\$5\$AOGM1KFw2Detl3xH\$40yCsKtsfhfmgVcLwVbt.mkY2zvZy0frUhIKas9L8b1' robot"
EXTRA_USERS_PARAMS += "usermod  -p '\$5\$A5KSOBt6MGQgp6ly\$Rm3EfxWdm8Ue/qJ2Gv0a3KTTy00Kqw5bVyT3QqZOi90' root;"

hostname:pn-base-files = "robot"
