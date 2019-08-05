import os
import unittest

from m2s.common.docker import Docker

class TestDocker(unittest.TestCase):

	test_base = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

	def test_from_yaml(self):
		yaml_path = os.path.join(self.test_base,
								 'common',
								 'data',
								 'm2s.yaml')

		docker = Docker.from_yaml(yaml_path)
		self.assertTrue(docker.project_name == 'test-project')
		self.assertTrue(docker.conda_env_name == 'test')
		self.assertTrue(docker.conda_env_file == 'environment.yaml')
		self.assertTrue(docker.modules == ['model.py'])
		self.assertTrue(docker.data == [])
		self.assertTrue(docker.pretrained == ['pretrained'])
		self.assertTrue(docker.service_startup_file == 'run_app.py')
		self.assertTrue(docker.service_app_name == 'service_app')