#!/usr/bin/env python3

'''
---------------------------------------------------------------
    xfconnect-indicator
    it is an AppIndicator for Kdeconnect in xfce environment.
    VERSION 0.5.0-1

    Copyright (C) 2013 Juan Ramon Castan Guillen <juanramoncastan@yahoo.es>

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
---------------------------------------------------------------
'''

import gi
import dbus
import os, sys, subprocess
import signal, time, datetime

from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import Gio as gio
from gi.repository import GLib
gi.require_version("Gdk", "3.0")
gi.require_version("Gtk", "3.0")

from gi.repository import Gdk as gdk
from gi.repository import Gtk as gtk

# Set to True to get console output control
DEBUG=False

def module_exists(module_name):
    try:
        gi.require_version(module_name, '0.1')
    except:
        return False
    else:
        return True

if module_exists('AppIndicator3'):
    from gi.repository import AppIndicator3 as appindicator
elif module_exists('AyatanaAppIndicator3'):
    from gi.repository import AyatanaAppIndicator3 as appindicator
else:
    print('Requires either AppIndicator3 or AyatanaAppIndicator3')
    exit(1)
    
    
    
####################################################################################

APPINDICATOR_NAME = 'xfceconnect-indicator'


class signalCatcher():
    def __init__(self, indicator):
        bus.add_signal_receiver(handler_function=indicator.signal_devices_changed, dbus_interface='org.kde.kdeconnect.daemon', signal_name='deviceListChanged', path_keyword='path', interface_keyword='iface', member_keyword='member')
        #bus.add_signal_receiver(handler_function=indicator.signal_devices_changed, dbus_interface='org.kde.kdeconnect.device', signal_name='reachableChanged', path_keyword='path', interface_keyword='iface', member_keyword='member')
        #bus.add_signal_receiver(handler_function=indicator.signal_devices_changed, dbus_interface='org.kde.kdeconnect.daemon', signal_name='deviceAdded', path_keyword='path', interface_keyword='iface', member_keyword='member')
        #bus.add_signal_receiver(handler_function=indicator.signal_devices_changed, dbus_interface='org.kde.kdeconnect.daemon', signal_name='deviceRemoved', path_keyword='path', interface_keyword='iface', member_keyword='member')
        #bus.add_signal_receiver(handler_function=indicator.echoSignal, dbus_interface='org.kde.kdeconnect.daemon', signal_name='customDevicesChanged', member_keyword='refresh')
        #bus.add_signal_receiver(handler_function=indicator.echoSignal, dbus_interface='org.kde.kdeconnect.daemon', signal_name='devicesVisibiityChanged', member_keyword='refresh')
        bus.add_signal_receiver(handler_function=indicator.signal_devices_changed, dbus_interface='org.kde.kdeconnect.daemon', signal_name='announcedNameChanged', path_keyword='path', interface_keyword='iface', member_keyword='member')
        bus.add_signal_receiver(handler_function=indicator.signal_devices_changed, dbus_interface='org.kde.kdeconnect.device', signal_name='nameChanged', path_keyword='path', interface_keyword='iface', member_keyword='member')
        bus.add_signal_receiver(handler_function=indicator.signal_battery, dbus_interface='org.kde.kdeconnect.device.battery', signal_name='refreshed', path_keyword='path', interface_keyword='iface', member_keyword='member')
        bus.add_signal_receiver(handler_function=indicator.signal_plugins_changed, dbus_interface='org.kde.kdeconnect.device', signal_name='pluginsChanged', path_keyword='path', interface_keyword='iface', member_keyword='member')
        bus.add_signal_receiver(handler_function=indicator.signal_mount, dbus_interface='org.kde.kdeconnect.device.sftp', signal_name='mounted',  path_keyword='path', interface_keyword='iface', member_keyword='member')
        bus.add_signal_receiver(handler_function=indicator.signal_mount, dbus_interface='org.kde.kdeconnect.device.sftp', signal_name='unmounted',  path_keyword='path', interface_keyword='iface', member_keyword='member')
        #bus.add_signal_receiver(handler_function=photo_received, dbus_interface='org.kde.kdeconnect.device.photo', signal_name='photoReceived')
        #bus.add_signal_receiver(handler_function=indicator.echoSignal, dbus_interface='org.kde.kdeconnect.device.connectivity_report', signal_name='refreshed')


class indicatorObject:
    def __init__(self, service):
        self.service=service
        mysignals = signalCatcher(self)
        self.icon_connected="xfconnect-icon"
        self.icon_disconnected="xfconnect-icon-disconnected"
        
        self.indicator = appindicator.Indicator.new(APPINDICATOR_NAME, self.icon_connected, appindicator.IndicatorCategory.SYSTEM_SERVICES)
        print(self.indicator.get_id()) if DEBUG else False # DEBUG
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_title('xfconnect')
        self.indicator.set_icon_full(self.icon_connected, 'xfconnect')
        self.deviceList={}
        self.menu=self.create_menu()
        self.get_devices()
        
        print(self.deviceList.keys()) if DEBUG else False # DEBUG
        
    def set_icon(self,icon):
        self.indicator.set_icon_full(icon,icon)

    def create_menu(self):
        menu = gtk.Menu()
        self.indicator.set_menu(menu)
        img = gtk.Image.new_from_icon_name('xfce4-settings', gtk.IconSize.MENU)
        item_configure = gtk.ImageMenuItem(image=img , label='Configure')
        self.add_menu(menu, item_configure, 2, self.kdecon_configure)
        #self.menu.append(item_configure)
        menu.append(gtk.SeparatorMenuItem())
        if not self.service:
            menu.append(gtk.SeparatorMenuItem())
            img_quit=gtk.Image.new_from_icon_name('gtk-quit', gtk.IconSize.MENU)
            item_quit=gtk.ImageMenuItem(image=img_quit, label='Quit')
            #item_quit.connect('activate', quit)
            self.add_menu(menu, item_quit, 4, quit)
        #self.menu.show_all()
        return menu
        
    def add_menu(self, menu, item, index=1, callback=None , data=None):
        if callback:
            item.connect('activate', callback, data)
        menu.insert(item, index)
        item.show()
        #self.menu.show_all()
        
    def get_devices(self):
        devices=self.dbus_method( 'org.kde.kdeconnect.daemon', '/modules/kdeconnect', 'org.kde.kdeconnect.daemon', 'deviceNames')
        print(devices) if DEBUG else False # DEBUG
        
        pairedDevices={}
        
        for key in list(self.deviceList):
            #if not key in pairedDevices:
            self.deviceList[key]['item_device'].destroy()
            del self.deviceList[key]
            
        for key in devices.keys():
            name=devices[key]
            device=key
            try:
                if self.dbus_property( 'org.kde.kdeconnect.daemon', '/modules/kdeconnect/devices/'+key, 'org.kde.kdeconnect.device', 'isTrusted' ):
                    pairedDevices[key] = name
            except:
                if self.dbus_property( 'org.kde.kdeconnect.daemon', '/modules/kdeconnect/devices/'+key, 'org.kde.kdeconnect.device', 'isPaired' ):
                    pairedDevices[key] = name

        pairedDevices=dict(sorted(pairedDevices.items(), key=lambda item: item[1].lower(), reverse=True)) # Sorted alphabetically
        active=False
        for key in pairedDevices.keys():
            charging=''
            charge=''
            
            name=pairedDevices[key]
            reachable=self.dbus_property( 'org.kde.kdeconnect.daemon', '/modules/kdeconnect/devices/'+key, 'org.kde.kdeconnect.device', 'isReachable' )


            self.deviceList[key]={}
            
            # Create menu Item
            self.deviceList[key]['item_device']=gtk.ImageMenuItem(image=None, label=name)
            self.deviceList[key]['name']=name
            self.item_sensitive(self.deviceList[key]['item_device'], reachable)
            self.add_menu(self.menu, self.deviceList[key]['item_device'], 2)
            
            self.create_device_menu(key)

            if reachable:
                self.update_battery(key)
                active=True
            
        self.menu.show_all()
        if active:
            self.indicator.set_icon_full(self.icon_connected, 'xfconnect')
        else:
            self.indicator.set_icon_full(self.icon_disconnected, 'xfconnect')
        return pairedDevices

    # Create a plugins submenu for every device
    def create_device_menu(self, device): 
        self.deviceList[device]['submenu']=gtk.Menu()
        self.deviceList[device]['item_device'].set_submenu(self.deviceList[device]['submenu'])
        
        if self.has_plugin(device, 'kdeconnect_battery'):
            self.deviceList[device]['kdeconnect_battery']=gtk.ImageMenuItem(image=None, label='Battery: ')
            self.add_menu(self.deviceList[device]['submenu'], self.deviceList[device]['kdeconnect_battery'], 1)
            self.item_sensitive(self.deviceList[device]['kdeconnect_battery'], self.is_plugin_enabled(device, 'kdeconnect_battery'))
            self.deviceList[device]['submenu'].append(gtk.SeparatorMenuItem())

        if self.has_plugin(device, 'kdeconnect_sftp'):
            self.deviceList[device]['kdeconnect_sftp']=gtk.ImageMenuItem(image=None, label='Browse remote')
            self.item_sensitive(self.deviceList[device]['kdeconnect_sftp'], self.is_plugin_enabled(device, 'kdeconnect_sftp'))
            self.add_menu(self.deviceList[device]['submenu'], self.deviceList[device]['kdeconnect_sftp'], 2)
            self.deviceList[device]['menu_mounted']=gtk.Menu()
            self.deviceList[device]['kdeconnect_sftp'].set_submenu(self.deviceList[device]['menu_mounted'])
            self.deviceList[device]['browse']=gtk.ImageMenuItem(image=None, label='Browse')
            self.add_menu(self.deviceList[device]['menu_mounted'], self.deviceList[device]['browse'], 1, self.browse, device)
            self.create_browse_menu(device)

        if self.has_plugin(device, 'kdeconnect_share'):
            self.deviceList[device]['kdeconnect_share']=gtk.ImageMenuItem(image=None, label='Send file...')
            self.add_menu(self.deviceList[device]['submenu'], self.deviceList[device]['kdeconnect_share'], 2, self.file_chooser, device)
            self.item_sensitive(self.deviceList[device]['kdeconnect_share'], self.is_plugin_enabled(device, 'kdeconnect_share'))
            
        if self.has_plugin(device,  'kdeconnect_share'):
            self.deviceList[device]['kdeconnect_findmyphone']=gtk.ImageMenuItem(image=None, label='Ring device')
            self.add_menu(self.deviceList[device]['submenu'], self.deviceList[device]['kdeconnect_findmyphone'], 2, self.ring, device)
            self.item_sensitive(self.deviceList[device]['kdeconnect_findmyphone'], self.is_plugin_enabled(device, 'kdeconnect_findmyphone'))
            
        if self.has_plugin(device,  'kdeconnect_clipboard'):
            self.deviceList[device]['kdeconnect_clipboard']=gtk.ImageMenuItem(image=None, label='Share clipboard')
            self.add_menu(self.deviceList[device]['submenu'], self.deviceList[device]['kdeconnect_clipboard'], 2, self.share_text, device)
            self.item_sensitive(self.deviceList[device]['kdeconnect_clipboard'], self.is_plugin_enabled(device, 'kdeconnect_clipboard'))

    # Create Browse submenu
    def create_browse_menu(self, device):
        if  self.is_mounted(device):
            self.deviceList[device]['unmount']=gtk.ImageMenuItem(image=None, label='Unmount')
            self.add_menu(self.deviceList[device]['menu_mounted'], self.deviceList[device]['unmount'], 1, self.unmount, device)
        else:
            try:
                self.deviceList[device]['unmount'].destroy()
                del self.deviceList[device]['unmount']
            except:
                False
        
    # Chack if plugin is enabled
    def is_plugin_enabled(self, device, plugin):
        return self.dbus_method( 'org.kde.kdeconnect.daemon', '/modules/kdeconnect/devices/'+device, 'org.kde.kdeconnect.device', 'isPluginEnabled', None, plugin )

    # Check if device has plugin
    def has_plugin(self, device, plugin):
        return self.dbus_method( 'org.kde.kdeconnect.daemon', '/modules/kdeconnect/devices/'+device, 'org.kde.kdeconnect.device', 'hasPlugin', None, plugin )
    
    # Get DBus method up to 2 arguments
    def dbus_method(self, obj, path, iface, method, mod=None, value1=None, value2=None):
        if mod:
            path=path+'/'+mod
            iface=iface+'.'+mod
        dbus_object=bus.get_object(obj,path)
        if not value2:
            answer=dbus_object.get_dbus_method(method, iface)(value1)
        else:
            answer=dbus_object.get_dbus_method(method, iface)(value1, value2)
        return answer
    
    # Get DBus property
    def dbus_property (self, obj, path, iface, prop, mod=None):
        if mod:
            path=path+'/'+mod
            iface=iface+'.'+mod
        dbus_object=bus.get_object(obj, path) 
        dbus_interface=dbus.Interface(dbus_object, 'org.freedesktop.DBus.Properties')
        propertie=dbus_interface.Get(iface, prop)
        return propertie

    # Make menu items sensitive
    def item_sensitive(self, item, reachable):
        if reachable:
            item.set_sensitive(True)
        else:
            item.set_sensitive(False)

    # Update battery menu item state
    def update_battery(self, device):
        charge=self.dbus_property( 'org.kde.kdeconnect.daemon', '/modules/kdeconnect/devices/'+device, 'org.kde.kdeconnect.device', 'charge', 'battery')
        chrg=self.dbus_property('org.kde.kdeconnect.daemon', '/modules/kdeconnect/devices/'+device, 'org.kde.kdeconnect.device',  'isCharging', 'battery')
        if chrg:
            charging='(charging)'
        else:
            charging='(wasting)'
            
        if charge < 0:
            charging=''
            charge=''
            
        charge=str(charge)+'%'
        charging
        self.deviceList[device]['kdeconnect_battery'].set_label('Battery: '+charge+' '+charging) # Sets the label of battery submenu item 

    # Open a window dialog to send files
    def file_chooser(self, widget, device):
        chooser=gtk.FileChooserDialog(title='Select files to send', parent=None, action=gtk.FileChooserAction.OPEN)
        chooser.set_current_folder(os.environ['HOME']) # Changing directory to $HOME
        chooser.set_select_multiple(True)
        chooser.add_button('_Open', gtk.ResponseType.OK)
        chooser.add_button('_Cancel', gtk.ResponseType.CANCEL)
        chooser.set_default_response(gtk.ResponseType.OK)
        if chooser.run() == gtk.ResponseType.OK:
            file_names=chooser.get_uris()
            chooser.destroy()
            for file in file_names:
                self.dbus_method('org.kde.kdeconnect.daemon', '/modules/kdeconnect/devices/'+device, 'org.kde.kdeconnect.device', 'shareUrl', 'share', file)
        chooser.destroy()

    # Ring remote phone
    def ring(self, widget, device):
        self.dbus_method('org.kde.kdeconnect.daemon', '/modules/kdeconnect/devices/'+device, 'org.kde.kdeconnect.device', 'ring', 'findmyphone')

    # Share clipboard
    def share_text(self, widget, device, text=None):
        clipboard=gtk.Clipboard.get(gdk.SELECTION_CLIPBOARD).wait_for_text()
        self.dbus_method('org.kde.kdeconnect.daemon', '/modules/kdeconnect/devices/'+device, 'org.kde.kdeconnect.device', 'shareText', 'share', clipboard)
        print(device) if DEBUG else False # DEBUG

    # Check if remote file system is mounted
    def is_mounted(self, device):  
        mounted=self.dbus_method('org.kde.kdeconnect.daemon', '/modules/kdeconnect/devices/'+device, 'org.kde.kdeconnect.device', 'isMounted', 'sftp')
        return mounted

    # Open a window to browse remote file system
    def browse(self, widget, device):
        mounted=self.is_mounted( device)
        if not mounted:
            self.dbus_method('org.kde.kdeconnect.daemon', '/modules/kdeconnect/devices/'+device, 'org.kde.kdeconnect.device', 'mount', 'sftp')
        mounted=self.dbus_method('org.kde.kdeconnect.daemon', '/modules/kdeconnect/devices/'+device, 'org.kde.kdeconnect.device', 'startBrowsing', 'sftp')
        print(mounted) if DEBUG else False # DEBUG

    # Unmount remote filesystem
    def unmount(self, widget, device):
        self.dbus_method('org.kde.kdeconnect.daemon', '/modules/kdeconnect/devices/'+device, 'org.kde.kdeconnect.device', 'unmount', 'sftp')


    ## Kdeconnect SIGNALS ###############
    # Signal if remote file system is mounted or unmounted
    def signal_mount(self, *args, **kwargs):
        device=kwargs['path'].split('/')[4]
        self.create_browse_menu(device)

    # Signal when plugins state changes
    def signal_plugins_changed(self, *args, **kwargs):
        device=kwargs['path'].split('/')[4]
        member=kwargs['member']
        self.deviceList[device]['submenu'].destroy()
        self.create_device_menu(device)

    # Signal if list of devices changes
    def signal_devices_changed(self, *args, **kwargs):
        # Update battery
        member=kwargs['member']
        devices=self.get_devices()
        if DEBUG: # DEBUG
            print(member)
            for d in devices: print(d)  

    # Signal when battery state of charge percent chnages
    def signal_battery(*args, **kwargs):
        # Update battery
        device=kwargs['path'].split('/')[4]
        iface=kwargs['iface']   
        if device:
            indicatorApp.update_battery(device)
            print(device) if DEBUG else False # DEBUG

    # Signal for test pourposes only
    def echo_signal(self, *args, **kwargs):
        print(kwargs) if DEBUG else False # DEBUG

    # Open kdeconnect configuration app
    def kdecon_configure(self, widget, data=None):
        try:
            dbus_object=bus.get_object('org.kde.kdeconnect.daemon', '/modules/kdeconnect')
            dbus_object.openConfiguration()
        except:
            os.system('kdeconnect-settings')

# Help message
def mssg_help():
    print('xfconnect-indicator.py')
    print('USAGE:\n\txfconnect-indicator.py [OPTIONS]')
    print('')
    print('OPTIONS:')
    print('\t-h Show this message.')
    print('\t-s It skips \"Quit\" option from menu.')
    print('\t   i.e. when it starts as service of systemd.')
    print('')
    exit()

# Close and destroy indicator
def quit( widget, source ):
    gtk.main_quit()


if __name__ == "__main__":
    # Check in args if it runs as service "-s" option
    service=False
    args=sys.argv
    for arg in args:
        print(arg) if DEBUG else False # DEBUG
        match arg:
            case '-s':
                service=True
            case '-h':
                mssg_help()
            case _:
                False

    # Changing directory to the Script root
    PATH_SCRIPT= os.path.dirname(os.path.realpath(__file__))
    os.chdir(PATH_SCRIPT)
    # Stting to catch signals and DBus signals
    DBusGMainLoop(set_as_default=True)
    bus = dbus.SessionBus()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    # Creating indicator object
    indicatorApp = indicatorObject(service) 
    
    gtk.main() # Gtk mainloop





