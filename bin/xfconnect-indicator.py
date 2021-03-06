#!/usr/bin/env python3

"""
This is a simple AppIndicator for Ubuntu used as an introduction to 
AppIndicators. Retrieves a random Pokemon name from a public API.
"""
import gi
import dbus
import os, sys, subprocess
import signal, time, datetime
import logging
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import Gio as gio
gi.require_version("Gdk", "3.0")
gi.require_version("Gtk", "3.0")
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gdk as gdk
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator


DEBUG=False

APPINDICATOR_NAME = 'Xfceconnect-indicator'

class indicatorObject:
    def __init__(self, icon_base):
        self.indicator = appindicator.Indicator.new(APPINDICATOR_NAME, os.path.abspath(icon_base), appindicator.IndicatorCategory.APPLICATION_STATUS)
        if DEBUG : print(self.indicator.get_id()) # Debug
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_title('Xfconnect')
        get_menu = build_menu_indicator()
        self.menu = get_menu[0]
        self.configureItem = get_menu[1]
        self.devices = {}
        self.indicator.set_menu(self.menu)
        
        kdecon_get_devices(self)

    def set_icon(self,icon):
        self.indicator.set_icon_full(os.path.abspath(icon),'')



class signalCatcher():
    def __init__(self):
        bus.add_signal_receiver(handler_function=echoSignal, dbus_interface = 'org.kde.kdeconnect.device', signal_name = 'reachableChanged')
        bus.add_signal_receiver(handler_function=echoSignal, dbus_interface = 'org.kde.kdeconnect.daemon', signal_name = 'deviceListChanged')
        bus.add_signal_receiver(handler_function=echoSignal, dbus_interface = 'org.kde.kdeconnect.device', signal_name = 'nameChanged')
        bus.add_signal_receiver(handler_function=echoSignal, dbus_interface = 'org.kde.kdeconnect.device.battery', signal_name = 'stateChanged')


def build_menu_indicator():
    menu = gtk.Menu()
    img_configure = gtk.Image.new_from_icon_name('xfce4-settings', gtk.IconSize.MENU)
    item_configure = gtk.ImageMenuItem(image=img_configure, label='Configure')
    item_configure.connect('activate', kdecon_configure)
    menu.append(item_configure)
    menu.show_all()
    
    return [menu,item_configure]


def kdecon_get_devices(indicator):
    dbus_object = bus.get_object('org.kde.kdeconnect.daemon','/modules/kdeconnect')
    dbus_interface = dbus.Interface(dbus_object, 'org.kde.kdeconnect.daemon')
    dev = dbus_interface.deviceNames()
    
    for key in list(indicator.devices.keys()):
        if not key in dev.keys() or not device_get_property(key,'isTrusted'):
            indicator.devices[key]['item'].destroy()
            del indicator.devices[key]
    
    if DEBUG : print('Devices:') # debug
    
    are_devices_connected = False
    for key in dev.keys():
        name = dev[key]
        connected = device_get_property(key,'isReachable')
        trusted = device_get_property(key,'isTrusted')
        charge = device_method(key,connected,'battery','charge')
        charging = device_method(key,connected,'battery','isCharging')
        if charging :
            chrg = '(charging)'
        else:
            chrg = '(wasting)'
        are_devices_connected = are_devices_connected or connected
        if trusted: 
            if key in indicator.devices.keys(): # If trusted device exists in devices{dictionary} we take items Gobjects
                # Takes stored values of Gojects in sub-dictionary
                item = indicator.devices[key]['item']
                #  Stored Gojects of submenu
                submenu = indicator.devices[key]['submenu']
                item_battery = indicator.devices[key]['item_battery']
                item_browse = indicator.devices[key]['item_browse']
                item_ring = indicator.devices[key]['item_ring']
                item_send_file = indicator.devices[key]['item_send_file']
                item_share_text = indicator.devices[key]['item_share_text']
            else: # If trusted device does NOT exists in devices dictionary we create new items for submenu
                # New sbubmenu
                submenu = gtk.Menu()
                # Device menu item
                img_device = gtk.Image.new_from_icon_name('stock-cell-phone', gtk.IconSize.MENU)
                item = gtk.ImageMenuItem(image=img_device, label=name)
                item.set_submenu(submenu)
                # Battery submenu item
                img_battery = gtk.Image.new_from_icon_name('battery', gtk.IconSize.MENU)
                item_battery = gtk.ImageMenuItem(image=img_battery, label='Battery: ')
                # Browse submenu item
                img_browse = gtk.Image.new_from_icon_name('folder', gtk.IconSize.MENU)
                item_browse = gtk.ImageMenuItem(image=img_browse, label='Browse')
                item_browse.connect('activate', browse, key)
                # Ring submenu item
                img_ring = gtk.Image.new_from_icon_name('stock_volume', gtk.IconSize.MENU)
                item_ring = gtk.ImageMenuItem(image=img_ring, label='Ring device')
                item_ring.connect('activate', ring, key)
                # Send file submenu item
                img_send_file = gtk.Image.new_from_icon_name('text-x-generic', gtk.IconSize.MENU)
                item_send_file = gtk.ImageMenuItem(image=img_send_file, label='Send file')
                item_send_file.connect('activate', file_chooser, key)
                # Share text submenu item
                img_share_text = gtk.Image.new_from_icon_name('gtk-paste', gtk.IconSize.MENU)
                item_share_text = gtk.ImageMenuItem(image=img_share_text, label='Share clipboard')
                item_share_text.connect('activate', share_text, key)
                # Append item to menu and items to submenu
                indicator.menu.append(item)
                submenu.append(item_battery)
                submenu.append(item_browse)
                submenu.append(item_ring)
                submenu.append(item_send_file)
                submenu.append(item_share_text)
                # Creates a new sub-dictionary  with values and its submenu items as Gobjects for the trusted device 
                indicator.devices[key] = {}
            
            
            item_battery.set_label('Batery: '+str(charge)+'% '+chrg) # Sets the label of battery submenu item 
            item_sensitive(item,connected) # State of clickabilty of device menu item
            indicator.menu.show_all()
            # Sets values of the sub-dictionary of this device (key)
            indicator.devices[key]['name'] = name 
            indicator.devices[key]['active'] = connected
            indicator.devices[key]['item'] = item
            indicator.devices[key]['battery'] = charge
            indicator.devices[key]['charging'] = charging
            indicator.devices[key]['submenu'] = submenu
            indicator.devices[key]['item_battery'] = item_battery
            indicator.devices[key]['item_browse'] = item_browse
            indicator.devices[key]['item_ring'] = item_ring
            indicator.devices[key]['item_send_file'] = item_send_file
            indicator.devices[key]['item_share_text'] = item_share_text

        if DEBUG : print('\t',key,'->',name,', Trusted: ',trusted,', Reachable: ', connected, ', Battery: ', charge ) # debug
           
    if are_devices_connected :
        indicator.set_icon('../share/xfconnect/xfconnect-icon.svg')
    else:
        indicator.set_icon('../share/xfconnect/xfconnect-icon-disconnected.svg')
        

def device_get_property(dev,prop):
    obj = 'org.kde.kdeconnect'
    path = '/modules/kdeconnect/devices/'+dev
    iface = 'org.kde.kdeconnect.device'
    dbus_object = bus.get_object(obj, path) 
    dbus_interface = dbus.Interface(dbus_object, 'org.freedesktop.DBus.Properties')
    prop_value = dbus_interface.Get(iface, prop)
    return prop_value


def device_method(dev, is_reachable=False, part=None, meth=None):
    obj = 'org.kde.kdeconnect'
    path = '/modules/kdeconnect/devices/'+dev
    iface = 'org.kde.kdeconnect.device'
    if is_reachable and part and meth:
        dbus_object = bus.get_object(obj, path) 
        dbus_interface = dbus.Interface(dbus_object, 'org.kde.kdeconnect.device.'+part)
        method = dbus_interface.get_dbus_method(meth)
        return method()
    else:
        return None

# Function for browse device file system
def browse(item,dev,): 
    obj = 'org.kde.kdeconnect'
    path = '/modules/kdeconnect/devices/'+dev+'/sftp'
    iface = 'org.kde.kdeconnect.device.sftp'
    try: # Mounting sftp using DBus
        dbus_object = bus.get_object(obj, path) 
        dbus_interface = dbus.Interface(dbus_object, iface)
        if not dbus_interface.isMounted():
            dbus_interface.mountAndWait() 
            time.sleep(0.15)
        mountpoint = dbus_interface.mountPoint()
    except Exception as Argument:
        timestamp = str(datetime.datetime.now())+" "
        f = open("/tmp/xfconnect.log", "a") 
        f.write(timestamp+str(Argument)+'\n') 
        f.close()
        
    browser_obj = 'org.xfce.Thunar'
    browser_path = '/org/xfce/FileManager'
    browser_iface = 'org.xfce.FileManager'
    try: # opening mount point in Thunar using DBus
        browser_object = bus.get_object(browser_obj, browser_path)
        browser_interface = dbus.Interface(browser_object, browser_iface)
        browser_interface.DisplayFolder(mountpoint, '', '')
    except Exception as Argument:
        timestamp = str(datetime.datetime.now())+" "
        f = open("/tmp/xfconnect.log", "a") 
        f.write(timestamp+str(Argument)+'\n') 
        f.close()

# Function t ring remote device
def ring(item,dev):
    obj = 'org.kde.kdeconnect'
    path = '/modules/kdeconnect/devices/'+dev+'/findmyphone'
    iface = 'org.kde.kdeconnect.device.findmyphone'
    try: # Ring the remote device with DBus
        dbus_object = bus.get_object(obj, path) 
        dbus_interface = dbus.Interface(dbus_object,iface)
        dbus_interface.ring()
    except Exception as Argument:
        timestamp = str(datetime.datetime.now())+" "
        f = open("/tmp/xfconnect.log", "a") 
        f.write(timestamp+str(Argument)+'\n') 
        f.close()

# Function to open file select dialog
def file_chooser(item,dev):
    chooser = gtk.FileChooserDialog(title="Select files to send", parent=None, action=gtk.FileChooserAction.OPEN)
    # Changing directory to $HOME
    chooser.set_current_folder(os.environ['HOME'])
    chooser.set_select_multiple(True)
    chooser.add_button("_Open", gtk.ResponseType.OK)
    chooser.add_button("_Cancel", gtk.ResponseType.CANCEL)
    chooser.set_default_response(gtk.ResponseType.OK)

    if chooser.run() == gtk.ResponseType.OK:
        file_names = chooser.get_uris()
        chooser.destroy()
        for f in file_names:
            send_file(dev,f)
    else:
        chooser.destroy()

# Function for send files to remote device
def send_file(dev,file_to_send):
    if DEBUG : print(file_names) # Debug
    obj = 'org.kde.kdeconnect'
    path = '/modules/kdeconnect/devices/'+dev+'/share'
    iface = 'org.kde.kdeconnect.device.share'
    try: # Sending files with DBus
        dbus_object = bus.get_object(obj, path) 
        dbus_interface = dbus.Interface(dbus_object,iface)
        dbus_interface.shareUrl(file_to_send)
    except Exception as Argument:
        timestamp = str(datetime.datetime.now())+" "
        f = open("/tmp/xfconnect.log", "a") 
        f.write(timestamp+str(Argument)+'\n') 
        f.close()

# Function for send text (clipboard) to device
def share_text(item,dev):
    cb = gtk.Clipboard.get(gdk.SELECTION_CLIPBOARD)
    obj = 'org.kde.kdeconnect'
    path = '/modules/kdeconnect/devices/'+dev+'/share'
    iface = 'org.kde.kdeconnect.device.share'
    try: # Sharing text with DBus
        dbus_object = bus.get_object(obj, path) 
        dbus_interface = dbus.Interface(dbus_object,iface)
        dbus_interface.shareText(cb.wait_for_text())
    except Exception as Argument:
        timestamp = str(datetime.datetime.now())+" "
        f = open("/tmp/xfconnect.log", "a") 
        f.write(timestamp+str(Argument)+'\n') 
        f.close()


def item_sensitive(item,connected):
    if connected :
        item.set_sensitive(True)
    else:
        item.set_sensitive(False)


def kdecon_configure(self):
    os.popen('kdeconnect-settings')


def echoSignal(*args, **kwargs):
    kdecon_get_devices(indicatorApp)


def quit(source):
    gtk.main_quit()


if __name__ == "__main__":
    # Changing directory to the Script root
    PATH_SCRIPT= os.path.dirname(os.path.realpath(__file__))
    os.chdir(PATH_SCRIPT)
    # Stting to catch signals and DBus signals
    DBusGMainLoop(set_as_default=True)
    bus = dbus.SessionBus()
    mysignals = signalCatcher()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    indicatorApp = indicatorObject('../share/xfconnect/xfconnect-icon.svg') # Creating indicator object
    gtk.main() # Gtk mainloop





