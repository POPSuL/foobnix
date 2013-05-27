# coding=utf-8
__author__ = 'popsul'

from gi.repository import Gtk
from gi.repository import Gdk
from foobnix.gui.plugins import BasePlugin


class Plugin(BasePlugin):

    def __init__(self):
        super(Plugin, self).__init__()
        self.context = None
        self.handler_id = None

    @staticmethod
    def get_name():
        return _("Copy info")

    @staticmethod
    def get_description():
        return _("Plugin for copy various info from playlists items.")

    @staticmethod
    def get_version():
        return 1, 0

    @staticmethod
    def get_dependencies():
        return BasePlugin.get_dependencies()

    def initialize(self, context):
        """ initialize(PluginContext) -> None """
        print("Infocopy initalized")
        self.context = context
        self.handler_id = self.context.get_event_dispatcher().connect("playlist-menu-extend", self.extend_menu)

    def destroy(self):
        print("Infocopy destroyed")
        self.context.get_event_dispatcher().disconnect(self.handler_id)
        self.context = None

    def extend_menu(self, dispatcher, menu, treeview):
        print("Infocopy extend menu", menu, treeview)
        menu.add_item(_('Copy №-Title-Time'), Gtk.STOCK_COPY,
                      lambda *a: self.copy_info_to_clipboard(treeview))
        menu.add_item(_('Copy Artist-Title-Album'), Gtk.STOCK_COPY,
                      lambda *a: self.copy_info_to_clipboard(treeview, True))
        menu.add_separator()

    def copy_info_to_clipboard(self, treeview, mode=False):
        print("Infocopy copy info", treeview, mode)
        beans = treeview.get_selected_beans()
        if not beans:
            return
        clb = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        if not mode:
            tracks = [b.tracknumber + ". " + b.title + " (" + b.time + ")"
                      if (b.tracknumber and b.title and b.time) else b.text for b in beans]
        else:
            tracks = []
            for bean in beans:
                artist = bean.artist if bean.artist else "Unknown artist"
                title = bean.title if bean.title else "Unknown title"
                album = bean.album if bean.album else "Unknown album"
                tracks.append(artist + " - " + title + " (" + album + ")")

        clb.set_text("\n".join(tracks), -1)