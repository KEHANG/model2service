import os
import argparse

from m2s.common.docker import Docker
from m2s.commands.base import BaseCommand

class DockerCommand(BaseCommand):
    name = "docker"

    def __init__(self, name):
        super(DockerCommand, self).__init__(name)
        self.show_in_help = True
        self.description = "Docker related commands."
        self.parser = argparse.ArgumentParser(
				            description=self.__class__.__doc__,
				            prog='m2s %s <yaml_path>' % (self.name),
				            usage='%(prog)s',
				            add_help=False)

    def execute(self, argv):
        if not argv:
            print("ERROR: Please specify a yaml file path.\n")
            self.help()
            return False

        yaml_path = argv[0]
        docker = Docker.from_yaml(yaml_path)

        output_path = os.path.dirname(yaml_path)
        docker.to_dockerfile(output_path)

command = DockerCommand.instance()