
path_build_robot := builds/build-rpi/tmp/deploy/images/raspberrypi3-64-robot
path_build_souris := builds/build-souris/tmp/deploy/images/raspberrypi0-w-robot
name_sdimg_robot := robot-image-raspberrypi3-64-robot.sdimg
name_sdimg_souris := souris-image-raspberrypi0-w-robot.sdimg
name_file_mender_robot := robot-image-raspberrypi3-64-robot.mender
name_file_mender_souris := souris-image-raspberrypi0-w-robot.mender
path_sd := /dev/sda

build:
	docker compose run --remove-orphans robot_yocto_dev bash -c "source layers/poky/oe-init-build-env builds/build-rpi/ && bitbake robot-image"

build/souris:
	docker compose run --remove-orphans robot_yocto_dev bash -c "source layers/poky/oe-init-build-env builds/build-souris/ && bitbake souris-image"

sdk:
	docker compose run --remove-orphans robot_yocto_dev bash -c "source layers/poky/oe-init-build-env builds/build-rpi/ && bitbake robot-image -c populate_sdk"

sdk/souris:
	docker compose run --remove-orphans robot_yocto_dev bash -c "source layers/poky/oe-init-build-env builds/build-souris/ && bitbake souris-image -c populate_sdk"

clean:
	docker compose run --remove-orphans robot_yocto_dev bash -c "source layers/poky/oe-init-build-env builds/build-rpi/ && bitbake -c clean robot-image"

flash:
	dd if=$(path_build_robot)/$(name_sdimg_robot) of=$(path_sd) bs=100M status=progress

flash/souris:
	dd if=$(path_build_souris)/$(name_sdimg_souris) of=$(path_sd) bs=100M status=progress

scp:
	scp $(path_build_robot)/$(name_file_mender_robot) root@$(ARGS):/tmp/.
	ssh root@$(ARGS) "mender-update install /tmp/$(name_file_mender_robot) && reboot"

	
scp/souris:
	scp $(path_build_souris)/$(name_file_mender_souris) root@$(ARGS):/tmp/.
	ssh root@$(ARGS) "mender-update install /tmp/$(name_file_mender_souris) && reboot"
