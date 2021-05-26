#!/bin/sh
set -x

# sometimes it will be slow... the author's website is getting busy
# you can run this script multiple times to make sure you've downloaded all model files.

# 2D 3D face landmark detectors
if ! echo "cd938726adb1f15f361263cce2db9cb820c42585fa8796ec72ce19107f369a46 2DFAN4-cd938726ad.zip" | sha256sum --check
then
    wget -O 2DFAN4-cd938726ad.zip https://www.adrianbulat.com/downloads/python-fan/2DFAN4-cd938726ad.zip
fi

if ! echo "4a694010b93140609b64a6ea734afc0ee80a4798394740281b0c5bea0ebef1d9  3DFAN4-4a694010b9.zip" | sha256sum --check
then
    wget -O 3DFAN4-4a694010b9.zip https://www.adrianbulat.com/downloads/python-fan/3DFAN4-4a694010b9.zip
fi

if ! echo "6c4283c0e0c5361854620610c2eba27f46a6ace1bfddb51dcc25264a94b038dc  depth-6c4283c0e0.zip" | sha256sum --check
then
    wget -O depth-6c4283c0e0.zip https://www.adrianbulat.com/downloads/python-fan/depth-6c4283c0e0.zip
fi

# SF3D face detector
if ! echo "619a31681264d3f7f7fc7a16a42cbbe8b23f31a256f75a366e5a1bcd59b33543  s3fd-619a316812.pth" | sha256sum --check
then
    wget -O s3fd-619a316812.pth https://www.adrianbulat.com/downloads/python-fan/s3fd-619a316812.pth
fi