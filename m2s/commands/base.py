
import six
import distutils.util

def add_argument(argument, type, default, help, argparser, **kwargs):
    type = distutils.util.strtobool if type == bool else type
    argparser.add_argument(
        argument,
        default=default,
        type=type,
        help=help + ' Default: %(default)s.' if help else help,
        **kwargs)

def print_arguments(args):
    print("-----------  Configuration Arguments -----------")
    for arg, value in sorted(six.iteritems(vars(args))):
        print("%s: %s" % (arg, value))
    print("------------------------------------------------")

class BaseCommand(object):
    """
    Base class for m2s commands

    Arguments:
        name (str): name of the command, also serving as 
        a key in command_dict (dict)
    """
    command_dict = {}

    @classmethod
    def instance(cls):
        if cls.name in BaseCommand.command_dict:
            command = BaseCommand.command_dict[cls.name]
            if command.__class__.__name__ != cls.__name__:
                raise KeyError(
                    "Command dict already has a command %s with type %s" %
                    (cls.name, command.__class__))
            return command
        if not hasattr(cls, '_instance'):
            cls._instance = cls(cls.name)
        BaseCommand.command_dict[cls.name] = cls._instance
        return cls._instance

    def __init__(self, name):
        if hasattr(self.__class__, '_instance'):
            raise RuntimeError("Please use `instance()` to get Command object!")
        self.args = None
        self.name = name
        self.show_in_help = True
        self.description = ""

    def help(self):
        """Prints help information for this command"""
        self.parser.print_help()

    def add_arg(self, argument, type="str", default=None, help=None):
        add_argument(
            argument=argument,
            type=type,
            default=default,
            help=help,
            argparser=self.parser)

    def print_args(self):
        print_arguments(self.args)

    def execute(self, argv):
        raise NotImplementedError("Base Command should not be executed!")