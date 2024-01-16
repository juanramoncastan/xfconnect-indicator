# ----------------------------------------------------------------------
#
#  Copyright (C) 2013 Juan Ramon Castan Guillen <juanramoncastan@yahoo.es>
#    
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
# ----------------------------------------------------------------------

# ###########      xfconnect-indicator Makefile     ###########################


# BUILD = "../package_name-version" given from "deb_package_creator" app

PREFIX = /usr
CONFIG_PATH = /etc
SRC_PATH = /src
BIN_PATH = /bin
SYSTEMD_PATH = /systemd/user
SHARE_PATH = /share


install: 
	mkdir -p  $(BUILD)$(PREFIX)$(BIN_PATH)
	mkdir -p  $(BUILD)$(CONFIG_PATH)$(SYSTEMD_PATH)/
	mkdir -p  $(BUILD)$(PREFIX)$(SHARE_PATH)/icons/
	sed -i  -e "s|\(ExecStart=\)\(.*\)|\1$(PREFIX)$(BIN_PATH)/xfconnect-indicator.py -s|" .$(SYSTEMD_PATH)/xfconnect.service
	cp .$(BIN_PATH)/xfconnect-indicator.py $(BUILD)$(PREFIX)$(BIN_PATH)/xfconnect-indicator.py
	cp .$(SYSTEMD_PATH)/xfconnect.service $(BUILD)$(CONFIG_PATH)$(SYSTEMD_PATH)/xfconnect.service
	cp .$(SHARE_PATH)/icons/* $(BUILD)$(PREFIX)$(SHARE_PATH)/icons/
	

uninstall:
	rm $(BUILD)$(PREFIX)$(BIN_PATH)/xfconnect-indicator.py
	rm $(BUILD)$(PREFIX)$(SHARE_PATH)/icons/xfconnect*
	rm $(BUILD)$(CONFIG_PATH)$(SYSTEMD_PATH)/xfconnect.service
