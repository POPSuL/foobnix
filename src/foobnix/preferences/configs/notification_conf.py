#-*- coding: utf-8 -*-
'''
Created on 3 сент. 2010

@author: ivan
'''
from foobnix.preferences.config_plugin import ConfigPlugin
import gtk
from foobnix.util.fc import FC
class NotificationConfig(ConfigPlugin):
    
    name = _("Notifications")
    
    def __init__(self, controls):
        box = gtk.VBox(False, 0)        
        box.hide()
        
        self.check_new_version = gtk.CheckButton(label=_("Check for new version on start"), use_underline=True)
        self.check_new_version.show()
        
        box.pack_start(self.check_new_version, False, True, 0)
        
        self.widget = box
    
    def on_load(self):
        self.check_new_version.set_active(FC().check_new_version)
    
    def on_save(self):        
        FC().check_new_version = self.check_new_version.get_active()
        
        
    
    
