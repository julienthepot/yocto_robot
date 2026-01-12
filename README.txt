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
`git clone git://git.yoctoproject.org/poky --branch scarthgap-5.0.13 --single-branch`

meta-raspberrypi :
`git clone git://git.yoctoproject.org/meta-raspberrypi --branch scarthgap --single-branch`

meta-openembedded-core : 
`git clone git://git.openembedded.org/meta-openembedded --branch scarthgap --single-branch`

meta-mender :
`git clone git://git.openembedded.org/meta-mender --branch scarthgap --single-branch`

meta-mender-community :
`git clone https://github.com/mendersoftware/meta-mender-community.git --branch scarthgap --single-branch`

meta-lts-mixins :
`git clone https://git.yoctoproject.org/meta-lts-mixins --branch scarthgap/u-boot --single-branch`

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

## Configuration Mender (OTA Updates)

### Qu'est-ce que Mender ?
Mender est un système de mise à jour Over-The-Air (OTA) open-source pour les systèmes embarqués Linux. Il permet de :
- Déployer des mises à jour à distance de manière sécurisée
- Effectuer un rollback automatique en cas d'échec
- Gérer des flottes de dispositifs
- Suivre l'état des déploiements

### Architecture Mender
Mender utilise un système à double partition (A/B):
- Partition A : Système actif
- Partition B : Partition de sauvegarde pour les mises à jour
- En cas d'échec, le système peut redémarrer sur l'ancienne partition

### Étapes d'intégration réalisées

1. **Ajout des layers Mender dans bblayers.conf**
   - `meta-mender-core` : Fonctionnalités principales de Mender
   - `meta-mender-raspberrypi` : Support spécifique pour Raspberry Pi

2. **Configuration dans local.conf**
   Les variables suivantes ont été ajoutées :
   - `INHERIT += "mender-full"` : Active toutes les fonctionnalités Mender
   - `MENDER_ARTIFACT_NAME` : Version de l'artefact (à incrémenter pour chaque nouvelle release)
   - `MENDER_DEVICE_TYPE` : Type de dispositif (raspberrypi3-64)
   - `MENDER_STORAGE_TOTAL_SIZE_MB` : Taille totale de la carte SD (128GB)
   - `MENDER_BOOT_PART_SIZE_MB` : Taille de la partition boot (256MB)
   - `MENDER_DATA_PART_SIZE_MB` : Taille de la partition data (20GB)
   - `RPI_USE_U_BOOT = "1"` : Active U-Boot (bootloader nécessaire pour Mender)
   - `IMAGE_FSTYPES` : Génère une image mender-sdimg au lieu de rpi-sdimg

### Build avec Mender

Compiler l'image avec Mender :
```bash
source layers/poky/oe-init-build-env builds/build-rpi/
bitbake robot-image
```

Les images générées se trouvent dans :
- `builds/build-rpi/tmp/deploy/images/raspberrypi3-64/robot-image-raspberrypi3-64.mender-sdimg` (image SD avec Mender)
- `builds/build-rpi/tmp/deploy/images/raspberrypi3-64/robot-image-raspberrypi3-64.mender` (artefact pour OTA)

### Flash l'image Mender sur la carte SD

```bash
sudo -s
lsblk  # identifier le device (ex: /dev/sdc)
umount /dev/sdc*  # démonter toutes les partitions
sudo dd if=builds/build-rpi/tmp/deploy/images/raspberrypi3-64/robot-image-raspberrypi3-64.sdimg of=/dev/sda bs=1G status=progress && sync
```

### Déploiement OTA avec Mender

#### Option 1 : Mender Server hébergé (hosted.mender.io)

1. Créer un compte sur https://hosted.mender.io
2. Obtenir le Tenant Token depuis la console Mender
3. Modifier dans `layers/robot/config/local.conf` :
```
MENDER_SERVER_URL = "https://hosted.mender.io"
MENDER_TENANT_TOKEN = "votre-token-ici"
```
4. Rebuild l'image
5. Déployer l'artefact `.mender` via l'interface web Mender

#### Option 2 : Serveur Mender local

1. Installer Mender Server localement (Docker):
```bash
git clone https://github.com/mendersoftware/mender-server.git
cd mender-server
./run up -d
```
2. Configurer dans local.conf :
```
MENDER_SERVER_URL = "https://your-server-ip"
```

#### Option 3 : Mode Standalone (sans serveur)

Pour tester localement sans serveur Mender :
1. Copier l'artefact `.mender` sur le device
2. Exécuter sur le Raspberry Pi :
```bash
mender-update install robot-image-raspberrypi3-64-1.0.0.mender
reboot
```

### Incrémenter la version pour une mise à jour

Avant chaque nouveau build OTA, modifier dans `local.conf` :
```
MENDER_ARTIFACT_NAME = "robot-image-1.0.1"  # Incrémenter la version
```

### Vérification sur le device

Une fois démarré, vérifier le statut Mender :
```bash
mender show-artifact  # Affiche la version installée
mender -version       # Version du client Mender
```

### Structure des partitions avec Mender

Avec Mender, la carte SD aura la structure suivante :
- `/dev/mmcblk0p1` : Partition boot (256MB)
- `/dev/mmcblk0p2` : Partition rootfs A (système actif)
- `/dev/mmcblk0p3` : Partition rootfs B (mise à jour)
- `/dev/mmcblk0p4` : Partition data (données persistantes)


bitbake robot-image -cdo_populate_sdk -Snone
bitbake robot-image -cdo_populate_sdk -Sprintdiff

bitbake-layers  add-layer  ../../layers/meta-openembedded/meta-oe/