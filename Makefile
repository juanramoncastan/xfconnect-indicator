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
#
# xfconnect-indicator.py
#
#
PREFIX = /usr/local
BIN = xfconnect-indicator.py
CONFIG_PATH = /etc
BIN_PATH = /bin
LAUNCH_PATH = /xdg/autostart
SYSTEMD_PATH = /systemd/user
SHARE_PATH = /share

install: 
	cp .$(BIN_PATH)/xfconnect-indicator.py $(PREFIX)$(BIN_PATH)/
	cp -R .$(SHARE_PATH)/xfconnect $(PREFIX)$(SHARE_PATH)/
	cp .$(SYSTEMD_PATH)/xfconnect.service $(CONFIG_PATH)$(SYSTEMD_PATH)/
	cp ./autostart/xfconnect-indicator.desktop $(CONFIG_PATH)$(LAUNCH_PATH)/

uninstall:
	rm $(PREFIX)$(BIN_PATH)/xfconnect-indicator.py
	rm -fR $(PREFIX)$(SHARE_PATH)/xfconnect
	rm $(CONFIG_PATH)$(SYSTEMD_PATH)/xfconnect.service
	rm $(CONFIG_PATH)$(LAUNCH_PATH)/xfconnect-indicator.desktop