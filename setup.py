# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "evaluation_server"
VERSION = "1.0.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "connexion",
    "swagger-ui-bundle>=0.0.2"
]

setup(
    name=NAME,
    version=VERSION,
    description="AI-LAB backend subject",
    author_email="ltyiz07@gmail.com",
    url="",
    keywords=["Swagger", "AI-LAB backend subject"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['swagger/swagger.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['evaluation_server=evaluation_server.__main__:main']},
    long_description="""\
    AI-model evaluate back-end API
    """
)
