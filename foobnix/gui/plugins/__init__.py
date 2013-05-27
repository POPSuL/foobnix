__author__ = 'popsul'

from gi.repository import GObject
from gi.repository import Gtk


class BasePlugin(GObject.GObject):

    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def get_name():
        raise NotImplementedError()

    @staticmethod
    def get_description():
        raise NotImplementedError()

    @staticmethod
    def get_version():
        return 1, 0

    @staticmethod
    def get_dependencies():
        return [("foobnix", (3, 0))]

    def initialize(self, context):
        pass

    def destroy(self):
        pass


class PluginContext:

    def __init__(self, plugin_manager, controls):
        self.plugin_manager = plugin_manager
        self.controls = controls

    def get_event_dispatcher(self):
        return self.plugin_manager.get_event_dispatcher()


class EventDispatcher(GObject.GObject):

    def __init__(self):
        super(EventDispatcher, self).__init__()

GObject.signal_new("playlist-menu-extend", EventDispatcher, GObject.SIGNAL_RUN_LAST, None, (Gtk.Menu, Gtk.TreeView))