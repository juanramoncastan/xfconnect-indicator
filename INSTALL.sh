#!/bin/bash


INSTALL_DIR="/usr/local/"

BIN_FILE="xfconnect-indicator.py"
BIN_FOLDER="bin/"
SHARE_FOLDER="share/xfconnect/"
SYSTEMD_FOLDER="systemd/user/"
AUTOSTART_FOLDER="autostart/"


if [ ! -e "${HOME}/.config/${AUTOSTART_FOLDER}" ]
then
    mkdir -p "${HOME}/.config/${AUTOSTART_FOLDER}"
fi
echo "Copying ${AUTOSTART_FOLDER}xfconnect-indicator.desktop"  "${HOME}/.config/${AUTOSTART_FOLDER}"
cp  "${AUTOSTART_FOLDER}xfconnect-indicator.desktop"  "${HOME}/.config/${AUTOSTART_FOLDER}"


if [ ! -e "${HOME}/.config/${SYSTEMD_FOLDER}" ]
then
    mkdir -p "${HOME}/.config/${SYSTEMD_FOLDER}"
fi
echo "Copying ${SYSTEMD_FOLDER}xfconnect.service"  "${HOME}/.config/${SYSTEMD_FOLDER}"
cp  "${SYSTEMD_FOLDER}xfconnect.service"  "${HOME}/.config/${SYSTEMD_FOLDER}"

if [ ! -e "${INSTALL_DIR}${BIN_FOLDER}" ]
then
    sudo mkdir -p "${INSTALL_DIR}${BIN_FOLDER}${BIN_FILE}"
fi
echo "Copying ${BIN_FILE} ${INSTALL_DIR}${BIN_FOLDER}${BIN_FILE}"
sudo cp ${BIN_FOLDER}${BIN_FILE} ${INSTALL_DIR}${BIN_FOLDER}${BIN_FILE}

echo


if [ ! -e "${INSTALL_DIR}${SHARE_FOLDER}" ]
then
    sudo mkdir -p "${INSTALL_DIR}${SHARE_FOLDER}"
fi
for IMG in $( ls -1  ${SHARE_FOLDER} )
do
    echo "Copying ${SHARE_FOLDER}$IMG ${INSTALL_DIR}${SHARE_FOLDER}$IMG"
    sudo cp -R ${SHARE_FOLDER}* ${INSTALL_DIR}${SHARE_FOLDER}
done
