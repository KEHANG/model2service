import os
from setuptools import find_packages, setup

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