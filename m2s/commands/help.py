

from m2s.commands.base import BaseCommand

class HelpCommand(BaseCommand):
    name = "help"

    def __init__(self, name):
        super(HelpCommand, self).__init__(name)
        self.show_in_help = True
        self.description = "Show help for commands."

    @classmethod
    def get_all_commands(cls):
        return BaseCommand.command_dict

    def execute(self, argv):
        m2s_command = BaseCommand.command_dict["m2s"]
        help_text = "\n"
        help_text += "Usage:\n"
        help_text += "%s <command> [options]\n" % m2s_command.name
        help_text += "\n"
        help_text += "Commands:\n"
        for _, command in self.get_all_commands().items():
            if not command.show_in_help or not command.description:
                continue
            help_text += "  %-15s\t\t%s\n" % (command.name, command.description)

        print(help_text)
        return True


command = HelpCommand.instance()