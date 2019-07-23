import os
import yaml

class Docker(object):
    """
    a ``Docker`` wraps an API service into a docker image.
    """
    def __init__(self,
                 project_name,
                 # environment related
                 conda_env_name,
                 conda_env_file,
                 # installation related
                 modules,
                 data,
                 pretrained,
                 # service startup related
                 service_startup_file,
                 service_app_name):
        """
        Arguments:
            project_name (str): name of the user application project
            conda_env_name (str): the name of conda environment
            conda_env_file (str): path to the environment yaml file of the project
            modules (list[str]): code modules for the project model
            data (list[str]): data folders needed for the project model to make prediction
            pretrained (list[str]): pretrained weight files of the project model
            service_startup_file (str): path to startup file of the service app
            service_app_name (str): the variable name of the service app in the startup file
        """
        self.project_name = project_name
        self.conda_env_name = conda_env_name
        self.conda_env_file = conda_env_file
        self.modules = modules
        self.data = data
        self.pretrained = pretrained
        self.service_startup_file = service_startup_file
        self.service_app_name = service_app_name

    @classmethod
    def from_yaml(cls, yaml_path):
        """
        Instantiate ``Docker`` class from a yaml file

        Arguments:
            yaml_path (str): path to the yaml file
        """
        with open(yaml_path, 'r') as stream:
            try:
                yaml_data = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

        project_name = yaml_data['project_name']
        conda_env_name = yaml_data['conda_env_name']
        conda_env_file = yaml_data['conda_env_file']
        modules = yaml_data['modules']
        data = yaml_data['data']
        pretrained = yaml_data['pretrained']
        service_startup_file = yaml_data['service_startup_file']
        service_app_name = yaml_data['service_app_name']

        return cls(project_name,
                   conda_env_name,
                   conda_env_file,
                   modules,
                   data,
                   pretrained,
                   service_startup_file,
                   service_app_name)

    def to_dockerfile(self, output_path):
        """
        This method generates Dockerfile based on the attributes
        of ``Docker`` instance.

        Arguments:
            output_path (str): directory for the output Dockerfile
        """
        env_var_str = f'ENV WS=/home/m2s_user/{self.project_name}'
        service_account_str = 'RUN adduser --disabled-password --gecos "" m2s_user'
        ws_declaration_str = """RUN mkdir -p $WS
WORKDIR $WS"""
        
        conda_env_str = f"""RUN mkdir envs
COPY {self.conda_env_file} envs/environment.yaml
RUN conda env create -f envs/environment.yaml"""
        
        startup_file_str = f"""COPY {self.service_startup_file} run_app.py
COPY launch_dk.sh ./
RUN chmod +x launch_dk.sh"""
        
        launch_str = """RUN chown -R m2s_user:m2s_user ./
USER m2s_user
EXPOSE 8000
ENTRYPOINT ["./launch_dk.sh"]"""
        
        modules_str = ''
        for module in self.modules:
            module_name = list(module.keys())[0]
            modules_str += f'RUN mkdir {module_name}\n'
            to_copy_files = module[module_name]
            for to_copy_file in to_copy_files:
                modules_str += f'COPY {to_copy_file} {module_name}/\n'
            modules_str += '\n'

        if len(self.data) > 0:
            data_str = "RUN mkdir data\n"
            for d in self.data:
                data_str += f'COPY {d} data/\n'
        else:
            data_str = ""

        if len(self.pretrained) > 0:
            pretrained_str = "RUN mkdir pretrained\n"
            for d in self.pretrained:
                pretrained_str += f'COPY {d} pretrained/\n'
        else:
            pretrained_str = ""

        dockerfile_str = f"""FROM continuumio/miniconda3:latest

# 1. set build-time environment variables
{env_var_str}

# 2. create service account
{service_account_str}

# 3. declare workspace
{ws_declaration_str}

# 4. create conda environment
{conda_env_str}

# 5.1 install application modules
{modules_str}
# 5.2 install application data
{data_str}
# 5.3 install pretrained model
{pretrained_str}
# 5.4 install startup files
{startup_file_str}

# 6. launch application
{launch_str}
"""

        launch_file_str = f"""#!/bin/bash
source activate {self.conda_env_name}
exec gunicorn -b :8000 --timeout 600 --access-logfile access.log --error-logfile error.log run_app:{self.service_app_name}
"""     
        dockerfile_path = os.path.join(output_path, 'Dockerfile')
        launch_file_path = os.path.join(output_path, 'launch_dk.sh')
        with open(dockerfile_path, 'w') as dockerfile:
            dockerfile.write(dockerfile_str)

        with open(launch_file_path, 'w') as launch_file:
            launch_file.write(launch_file_str)
