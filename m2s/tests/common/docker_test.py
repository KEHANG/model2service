import os
import unittest

from m2s.common.docker import Docker

class TestDocker(unittest.TestCase):

    def setUp(self):
        test_base = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        self.yaml_path1 = os.path.join(test_base, 'common', 'data', 'm2s_1.yaml')
        self.docker1 = Docker.from_yaml(self.yaml_path1)

        self.yaml_path2 = os.path.join(test_base, 'common', 'data', 'm2s_2.yaml')
        self.docker2 = Docker.from_yaml(self.yaml_path2)

    def test_from_yaml(self):
        
        self.assertTrue(self.docker1.project_name == 'test-project')
        self.assertTrue(self.docker1.conda_env_name == 'test')
        self.assertTrue(self.docker1.conda_env_file == 'environment.yaml')
        self.assertTrue(self.docker1.modules == ['model.py'])
        self.assertTrue(self.docker1.data == [])
        self.assertTrue(self.docker1.pretrained == ['pretrained'])
        self.assertTrue(self.docker1.service_startup_file == 'run_app.py')
        self.assertTrue(self.docker1.service_app_name == 'service_app')

    def test_generate_modules_str(self):

        modules_str = self.docker2.generate_modules_str()
        expected_modules_str = """RUN mkdir module1
COPY module1 module1/
RUN mkdir module2
COPY module2 module2/
"""
        self.assertTrue(modules_str == expected_modules_str)

    def test_generate_data_str(self):

        data_str = self.docker2.generate_data_str()
        expected_data_str = """RUN mkdir data
COPY data/meta_data.csv data/
"""
        self.assertTrue(data_str == expected_data_str)

    def test_generate_pretrained_str(self):

        pretrained_str = self.docker2.generate_pretrained_str()
        expected_pretrained_str = ""
        self.assertTrue(pretrained_str == expected_pretrained_str)

    def test_to_dockerfile(self):

        output_path = os.path.dirname(self.yaml_path1)
        dockerfile_str, launch_file_str = self.docker1.to_dockerfile(output_path)

        expected_dockerfile_str = """FROM continuumio/miniconda3:latest

# 1. set build-time environment variables
ENV WS=/home/m2s_user/test-project

# 2. create service account
RUN adduser --disabled-password --gecos "" m2s_user

# 3. declare workspace
RUN mkdir -p $WS
WORKDIR $WS

# 4. create conda environment
RUN mkdir envs
COPY environment.yaml envs/environment.yaml
RUN conda env create -f envs/environment.yaml

# 5.1 install application modules
COPY model.py ./

# 5.2 install application data

# 5.3 install pretrained model
RUN mkdir pretrained
COPY pretrained pretrained/

# 5.4 install startup files
COPY run_app.py run_app.py
COPY launch_dk.sh ./
RUN chmod +x launch_dk.sh

# 6. launch application
RUN chown -R m2s_user:m2s_user ./
USER m2s_user
EXPOSE 8000
ENTRYPOINT ["./launch_dk.sh"]"""

        expected_launch_file_str = """#!/bin/bash
source activate test
exec gunicorn -b :8000 --timeout 600 --access-logfile access.log --error-logfile error.log run_app:service_app"""
        self.assertTrue(dockerfile_str == expected_dockerfile_str)
        self.assertTrue(launch_file_str == expected_launch_file_str)
        os.remove(os.path.join(output_path, 'Dockerfile'))
        os.remove(os.path.join(output_path, 'launch_dk.sh'))

