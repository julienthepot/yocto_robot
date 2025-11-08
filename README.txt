# Yocto 
## Build
```
docker compose build robot_yocto_dev
```

## Launch l'environnement de developpement dans le docker
```
docker compose run robot_yocto_dev
```

Puis déplacer vous dans le repertoire de yocto (binaire/yocto) pour executer les différentes commandes

## Info

poky :
`git clone git://git.yoctoproject.org/poky --branch scarthgap-5.0.6 --single-branch`   

meta-raspberrypi :
`git clone git://git.yoctoproject.org/meta-raspberrypi --branch scarthgap --single-branch`

meta-openembedded-core : 
`git clone git://git.openembedded.org/meta-openembedded --branch scarthgap --single-branch`

source du fichier yocto (poky)
deux dossiers de build possible (builds/build-rpi ou builds/build-qemu) 
```
source layers/poky/oe-init-build-env builds/build-rpi/
```

ajout d'une nouvelle layer
```
# etre dans le dossier de build
bitbake add-layer ../../layers/<layer-name>
```


compile image in docker
```
bitbake robot-image
```

generate sdk in docker
```
bitbake -c populate_sdk robot-image
```

launch qemu in docker 
```
  cd ${build_folder}
  runqemu slirp no graphic
```

quit an qemu application 
Ctr + A puis X 

flash une image
localisation : build-rpi/tmp/deploy/images/raspberrypi3-64/core-image-minimal-raspberrypi3-64.wic.bz2
commande pour flash :
```
sudo -s
lsblk => permet de savoir où est le device
umount "emplacement du device" => exemple : sudo umount /dev/sda?
bzcat "nom de l'image" > "emplacement du device"
sudo dd if="builds/build-rpi/tmp/deploy/images/raspberrypi3-64/robot-image-raspberrypi3-64.rootfs.wic" of="/dev/sdc" status=progress
```


bitbake robot-image -cdo_populate_sdk -Snone
bitbake robot-image -cdo_populate_sdk -Sprintdiff

bitbake-layers  add-layer  ../../layers/meta-openembedded/meta-oe/