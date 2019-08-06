import os
import unittest

from m2s.common.docker import Docker

class TestDocker(unittest.TestCase):

    def setUp(self):
        test_base = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        self.yaml_path = os.path.join(test_base, 'common', 'data', 'm2s.yaml')
        self.docker = Docker.from_yaml(self.yaml_path)

    def test_from_yaml(self):
        
        self.assertTrue(self.docker.project_name == 'test-project')
        self.assertTrue(self.docker.conda_env_name == 'test')
        self.assertTrue(self.docker.conda_env_file == 'environment.yaml')
        self.assertTrue(self.docker.modules == ['model.py'])
        self.assertTrue(self.docker.data == [])
        self.assertTrue(self.docker.pretrained == ['pretrained'])
        self.assertTrue(self.docker.service_startup_file == 'run_app.py')
        self.assertTrue(self.docker.service_app_name == 'service_app')

    def test_to_dockerfile(self):