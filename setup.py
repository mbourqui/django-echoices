#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import find_packages, setup

from echoices import __version__

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-echoices',
    version=__version__,
    author='Marc Bourqui',
    author_email='https://github.com/mbourqui',
    license='GNU GPLv3',
    description='Choices for Django model fields as enumeration',
    long_description=README,
    url='https://github.com/mbourqui/django-echoices',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['*.po', '*.mo'],
    },
    install_requires=[
        'Django>=1.9.13',
    ],
    keywords='django choices models enum',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Utilities',
    ],
)
