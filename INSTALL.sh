#!/bin/bash


INSTALL_DIR="/usr/local/"

BIN_FILE="bin/xfconnect-indicator.py"
SHARE_FOLDER="share/xfconnect/"
SYSTEMD_SERVICE="systemd/user/"

#mkdir -p "${HOME}/.config/${SYSTEMD_SERVICE}"
echo "Copying ${SYSTEMD_SERVICE}xfconnect.service"  "${HOME}/.config"
cp --parents ${SYSTEMD_SERVICE}xfconnect.service ${HOME}/.config

echo "Copying ${BIN_FILE} ${INSTALL_DIR}${BIN_FILE}"
#mkdir -p "${INSTALL_DIR}${BIN_FILE}"
sudo cp ${BIN_FILE} ${INSTALL_DIR}${BIN_FILE}

echo "Copying ${SHARE_FOLDER} ${INSTALL_DIR}${SHARE_FOLDER}"
#mkdir -p "${INSTALL_DIR}${SHARE_FOLDER}"
sudo cp -R ${SHARE_FOLDER} ${INSTALL_DIR}${SHARE_FOLDER}
