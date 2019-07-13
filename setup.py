import os
from setuptools import find_packages, setup

modules = []
for root, dirs, files in os.walk('m2s'):
    for file in files:
        if file.endswith('.py'):
            if 'test' not in file and '__init__' not in file:
                module = 'm2s' + root.partition('m2s')[-1].replace('/','.') + '.' + file.partition('.py')[0]
                modules.append(module)

exec(open('m2s/version.py').read())

setup(
    name='Model2Service',
    version=m2s_version,
    packages=find_packages(exclude=["tests"]),
    description='A humble tool that bridges data science models and services.',
    author='Kehang Han',
    author_email='kehanghan@gmail.com',
    entry_points={'console_scripts': ['m2s=m2s.commands.main:main']}
)