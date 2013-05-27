__author__ = 'popsul'


from foobnix.gui.plugins import BasePlugin


class Plugin(BasePlugin):

    def __init__(self):
        super(Plugin, self).__init__()

    @staticmethod
    def get_name():
        return "Example plugin"

    @staticmethod
    def get_description():
        return "Dummy plugin example for developers"

    @staticmethod
    def get_version():
        return 1, 0, 1

    @staticmethod
    def get_dependencies():
        return BasePlugin.get_dependencies()
