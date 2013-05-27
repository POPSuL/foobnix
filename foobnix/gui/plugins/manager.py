__author__ = 'popsul'

import os
import sys
import pkgutil
import importlib

from . import BasePlugin
from . import EventDispatcher
from . import PluginContext
from .gui_manager import GUIManager
from gi.repository import GObject
from foobnix.gui.state import LoadSave
from foobnix.gui.base_controls import BaseFoobnixControls


class Manager(GObject.GObject, LoadSave):

    def __init__(self, controls):
        super(Manager, self).__init__()
        #assert isinstance(controls, BaseFoobnixControls)
        self.controls = controls
        self.loaded_plugins = {}
        self.active_plugins = []
        user_plugins = os.path.expanduser("~/.config/foobnix/plugins")
        if not os.path.exists(user_plugins):
            os.makedirs(user_plugins)
        sys.path.append(user_plugins)
        self.event_dispatcher = EventDispatcher()

    def list_plugins(self):
        package = "foobnix.plugins."
        return [name for i, name, ispackage in pkgutil.iter_modules([package.replace(".", "/")], package) if ispackage]

    def is_loaded(self, package):
        return package in self.loaded_plugins

    def load_plugin(self, package):
        if self.is_loaded(package):
            return True
        try:
            module = importlib.import_module(package)
        except ImportError:
            return False
        if "Plugin" in module.__dict__:
            instance = module.Plugin()
            if isinstance(instance, BasePlugin):
                self.loaded_plugins[package] = instance
            else:
                del instance
            return True
        return False

    def get_plugin_instance(self, package):
        """ get_plugin_instance(str) -> BasePlugin """
        if self.load_plugin(package):
            return self.loaded_plugins[package]
        return None

    def get_plugin_info(self, package):
        plugin = self.get_plugin_instance(package)
        if not plugin:
            return None
        return plugin.get_name(), plugin.get_description(), plugin.get_version(), plugin.get_dependencies()

    def activate_plugin(self, package):
        print ("activate_plugin(%s)" % package)
        if package in self.active_plugins:
            print ("Already active")
            return True

        plugin = self.get_plugin_instance(package)
        print("Plugin instance is", plugin)
        try:
            plugin.initialize(PluginContext(self, self.controls))
            self.active_plugins.append(package)
            return True
        except Exception as e:
            return False

    def deactivate_plugin(self, package):
        if package not in self.active_plugins:
            return True
        plugin = self.get_plugin_instance(package)
        try:
            plugin.destroy()
            self.active_plugins.remove(package)
            return True
        except:
            return False

    def get_event_dispatcher(self):
        return self.event_dispatcher

    def show_plugins(self, *args):
        popup = GUIManager(self)
        popup.run()

    def on_load(self):
        for plugin in self.list_plugins():
            try:
                print("Load plugin", plugin)
                self.activate_plugin(plugin)
                print("Plugin loaded")
            except Exception as e:
                print (e)

if __name__ == "__main__":
    manager = Manager(None)
    print(manager.list_plugins())