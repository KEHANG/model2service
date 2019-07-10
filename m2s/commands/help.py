

from m2s.commands.base import BaseCommand

class HelpCommand(BaseCommand):
    name = "help"

    def __init__(self, name):
        super(HelpCommand, self).__init__(name)
        self.show_in_help = True
        self.description = "Show help for commands."

    def get_all_commands(self):
        return BaseCommand.command_dict

    def execute(self, argv):
        m2s_command = BaseCommand.command_dict["m2s"]
        help_text = "\n"
        help_text += "Usage:\n"
        help_text += "%s <command> [options]\n" % m2s_command.name
        help_text += "\n"
        help_text += "Commands:\n"
        for command_name, command in self.get_all_commands().items():
            if not command.show_in_help or not command.description:
                continue
            help_text += "  %-15s\t\t%s\n" % (command.name, command.description)

        print(help_text)
        return True


command = HelpCommand.instance()