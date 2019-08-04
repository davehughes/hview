import os
import ConfigParser

from setuptools import find_packages, setup


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


def version_from_setup_cfg():
    config = ConfigParser.ConfigParser()
    config.read(os.path.join(PROJECT_ROOT, 'tox.ini'))


setup(
    name='hview',
    version=version_from_setup_cfg(),
    description='Hierarchical data viewer and utilities',

    packages=find_packages(),
    install_requires=[
        'jinja2',
        'pathspec',
    ],

    entry_points={
        'console_scripts': [
            'hview=hview.cli:main',
        ],
    },
)
