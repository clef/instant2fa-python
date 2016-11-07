#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "requests>=2.11.1, <3.0"
]

test_requirements = [
    # TODO: put package test requirements here
    "mock==2.0.0",
    "pytest",
    "requests_mock>=1.1.0, <2.0"
]

setup(
    name='instant2fa',
    version='1.0.0',
    description="Instant2FA Python bindings.",
    long_description=readme + '\n\n' + history,
    author="Grace Wong",
    author_email='grace@getclef.com',
    url='https://github.com/clef/instant2fa-python',
    packages=[
        'instant2fa',
    ],
    package_dir={'instant2fa':
                 'instant2fa'},
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='instant2fa',
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=['pytest-runner']
)
