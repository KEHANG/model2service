import yaml

class Docker(object):
    """
    a ``Docker`` wraps an API service into a docker image.
    """
    def __init__(self,
                 project_name,
                 # environment related
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
            conda_env_file (str): path to the environment yaml file of the project
            modules (list[str]): code modules for the project model
            data (list[str]): data folders needed for the project model to make prediction
            pretrained (list[str]): pretrained weight files of the project model
            service_startup_file (str): path to startup file of the service app
            service_app_name (str): the variable name of the service app in the startup file
        """
        self.project_name = project_name
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
        conda_env_file = yaml_data['conda_env_file']
        modules = yaml_data['modules']
        data = yaml_data['data']
        pretrained = yaml_data['pretrained']
        service_startup_file = yaml_data['service_startup_file']
        service_app_name = yaml_data['service_app_name']

        return cls(project_name,
                   conda_env_file,
                   modules,
                   data,
                   pretrained,
                   service_startup_file,
                   service_app_name)

    def to_dockerfile(self, dockerfile_path):
        """
        This method generates Dockerfile based on the attributes
        of ``Docker`` instance.

        Arguments:
            dockerfile_path (str): output path to the generated Dockerfile
        """
        modules_str = ""
        for m in self.modules:
            modules_str += f'COPY {m} {m}\n'

        data_str = ""
        for d in self.data:
            data_str += f'COPY {d} {d}\n'

        pretrained_str = ""
        for p in self.pretrained:
            pretrained_str += f'COPY {p} {p}\n'

        dockerfile_str = f"""FROM continuumio/miniconda3:latest

# 1. set build-time environment variables
ENV WS=/home/m2s_user/{self.project_name}

# 2. create service account
RUN adduser --disabled-password --gecos "" m2s_user

# 3. declare workspace
RUN mkdir -p $WS
WORKDIR $WS

# 4. create conda environment
RUN mkdir envs
COPY {self.conda_env_file} envs/environment.yaml
RUN conda env create -f envs/environment.yaml

# 5.1 install application modules
{modules_str}

# 5.2 install application data
RUN mkdir data
{data_str}

# 5.3 install pretrained model
RUN mkdir pretrained
{pretrained_str}

# 5.4 install startup files
COPY {self.service_startup_file} ./
COPY launch_dk.sh ./
RUN chmod +x launch_dk.sh

# 6. launch application
RUN chown -R m2s_user:m2s_user ./
USER m2s_user
EXPOSE 8000
ENTRYPOINT ["./launch_dk.sh"]
"""
        with open(dockerfile_path, 'w') as dockerfile:
            dockerfile.write(dockerfile_str)
