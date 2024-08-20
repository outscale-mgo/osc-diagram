# -*- coding: utf-8 -*-
import setuptools
import os

def get_long_description():
    root_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(root_path, 'README.md'), 'r') as fd:
        return fd.read()

def get_version():
    root_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(root_path, 'osc_diagram', 'VERSION'), 'r') as fd:
        return fd.read().strip()

setuptools.setup(
    name='osc-diagram',
    version=get_version(),
    author="Outscal SAS",
    author_email="opensource@outscale.com",
    description="Outscale Gateway python SDK",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://github.com/outscale-mgo/osc-diagram",
    packages=setuptools.find_packages(),
    entry_points={"console_scripts": ["osc-diagram = osc_diagram.main:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "osc-sdk-python>=0.22.0",
        'diagrams>=0.23.3'
    ]
)
