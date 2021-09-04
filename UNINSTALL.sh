#!/bin/bash


INSTALL_DIR="/usr/local/"

BIN_FILE="xfconnect-indicator.py"
BIN_FOLDER="bin/"
SHARE_FOLDER="share/xfconnect/"
SYSTEMD_FOLDER="systemd/user/"



echo "Deleting ${HOME}/.config/${AUTOSTART_FOLDER}xfconnect-indicator.desktop"
rm  "${HOME}/.config/${AUTOSTART_FOLDER}xfconnect-indicator.desktop"


echo "Deleting ${HOME}/.config/${SYSTEMD_FOLDER}xfconnect.service"
rm  "${HOME}/.config/${SYSTEMD_FOLDER}xfconnect.service"


echo "Deleting ${INSTALL_DIR}${BIN_FOLDER}${BIN_FILE}"
sudo rm  "${INSTALL_DIR}${BIN_FOLDER}${BIN_FILE}"


echo "Deleting  ${INSTALL_DIR}${SHARE_FOLDER}"
sudo rm -R ${INSTALL_DIR}${SHARE_FOLDER}

