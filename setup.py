# -*- coding: utf-8 -*-
"""setup for pathfinder package."""
from setuptools import find_packages
from setuptools import setup

setup(
    name="pathfinder",
    description="pathfinder – a simpler os.walk",
    long_description=open("README.rst").read(),
    url="http://jkeyes.github.com/pathfinder/",
    author="John Keyes",
    author_email="john@keyes.ie",
    version="0.6.0",
    license="MIT License",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    packages=find_packages(),
)
