poky :
`git clone git://git.yoctoproject.org/poky --branch kirkstone-4.0.13 --single-branch`   

meta-raspberrypi :
`git clone git://git.yoctoproject.org/meta-raspberrypi --branch kirkstone --single-branch`

meta-openembedded-core : 
`git clone git://git.openembedded.org/meta-openembedded --branch 2022-04.13-kirkstone --single-branch`

meta-ros : 
`git clone https://github.com/ros/meta-ros.git --branch kirkstone --single-branch`

meta-qt : 
`git clone https://github.com/meta-qt5/meta-qt5.git --branch kirkstone --single-branch`


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
```


bitbake robot-image -cdo_populate_sdk -Snone
bitbake robot-image -cdo_populate_sdk -Sprintdiff