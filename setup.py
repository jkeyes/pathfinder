#
# Copyright 2012 John Keyes
#
# http://jkeyes.mit-license.org/
#

from setuptools import find_packages
from setuptools import setup

setup(name='pathfinder',
    description='Pathfinder os.walk for humans',
    long_description=open('README.rst').read(),
    url='http://jkeyes.github.com/pathfinder/',
    author='John Keyes',
    author_email='john@keyes.ie',
    version='0.5.3',
    license='MIT License',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    packages=find_packages()
)