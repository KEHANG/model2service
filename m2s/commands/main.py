import sys

from m2s.commands import help
from m2s.commands import version
from m2s.commands.base import BaseCommand


class M2sCommand(BaseCommand):
    name = "m2s"

    def __init__(self, name):
        super(M2sCommand, self).__init__(name)
        self.show_in_help = False

    def execute(self, argv):
        if not argv:
            help.command.execute(argv)
            exit(1)
            return False
        sub_command = argv[0]
        if not sub_command in BaseCommand.command_dict:
            print("ERROR: unknown command '%s'" % sub_command)
            help.command.execute(argv)
            exit(1)
            return False
        command = BaseCommand.command_dict[sub_command]
        return command.execute(argv[1:])

command = M2sCommand.instance()

def main():
    argv = []
    for item in sys.argv:
        argv.append(item)
    command.execute(argv[1:])

if __name__ == '__main__':
	main()