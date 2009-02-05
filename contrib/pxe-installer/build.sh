#!/bin/sh

set -e
set -x

OS=lenny-root
debootstrap lenny $OS http://compil:9999/debian
chroot $OS apt-get install linux-image-2.6.26-1-686 pciutils partimage parted
mv $OS/boot/vmli* .
rm -f $OS/boot/init*
rm -rf $OS/usr/share/{man,info,locale}
cp init $OS/
