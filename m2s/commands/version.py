
from m2s import version
from m2s.commands.base import BaseCommand

class VersionCommand(BaseCommand):
    name = "version"

    def __init__(self, name):
        super(VersionCommand, self).__init__(name)
        self.show_in_help = True
        self.description = "Show Model2Service version."

    def execute(self, argv):
        print("m2s %s" % version.m2s_version)
        return True

command = VersionCommand.instance()