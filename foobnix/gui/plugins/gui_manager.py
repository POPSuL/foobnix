
__author__ = 'popsul'

from gi.repository import Gtk
from gi.repository import GObject

from foobnix.gui.model import FDModel
from foobnix.util.const import ICON_FOOBNIX
from foobnix.gui.perspectives import StackableWidget
from foobnix.gui.treeview.simple_tree import SimpleListTreeControl
from foobnix.gui.service.path_service import get_foobnix_resourse_path_by_name


class GUIManager(Gtk.Dialog):

    def __init__(self, manager):
        super(GUIManager, self).__init__(_("Plugins"), None, Gtk.DialogFlags.MODAL, ())
        self.manager = manager
        self.assocs = {}
        self.init_gui()
        self.fill_plugin_list()

    def init_gui(self):
        self.paned = Gtk.HPaned()
        self.paned.set_position(250)

        self.plugin_list = SimpleListTreeControl(_("Plugins"), None, True)
        self.plugin_list.set_left_click_func(self.show_plugin_info)

        self.stackable = StackableWidget()
        self.stackable.add(Gtk.Label(_("Select plugin")))

        self.paned.add1(self.plugin_list.scroll)
        self.paned.add2(self.stackable)
        self.vbox.pack_start(self.paned, True, True, 0)
        try:
            self.set_icon_from_file(get_foobnix_resourse_path_by_name(ICON_FOOBNIX))
        except TypeError:
            pass
        self.set_size_request(550, 200)
        self.show_all()

    def fill_plugin_list(self):
        plugins = self.manager.list_plugins()
        for plugin in plugins:
            info = self.manager.get_plugin_info(plugin)
            self.plugin_list.append(FDModel(info[0], plugin))

    def show_plugin_info(self, *args):
        print("show plugin info")
        plugin = self.plugin_list.get_selected_bean()

        if plugin.path in self.assocs:
            self.stackable.set_active_by_index(self.assocs[plugin.path])
        else:
            index = self.stackable.add(self._create_plugin_info(plugin.path))
            self.assocs[plugin.path] = index
            self.stackable.set_active_by_index(self.assocs[plugin.path])

    def _create_plugin_info(self, plugin):
        info = self.manager.get_plugin_info(plugin)
        vbox = Gtk.VBox(False, 0)
        title = Gtk.Label(info[0])
        separator = Gtk.HSeparator()
        description = Gtk.Label(info[1])
        version = Gtk.Label(info[2])
        vbox.pack_start(title, False, False, 0)
        vbox.pack_start(separator, False, False, 0)
        vbox.pack_start(description, False, False, 0)
        vbox.pack_start(version, False, False, 0)
        vbox.show_all()
        return vbox