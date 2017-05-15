#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'tqdm',
    'requests',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='kolla_dockerhub_pusher',
    version='0.1.0',
    description="Small set of scripts to manage kolla dockerhub",
    long_description=readme + '\n\n' + history,
    author="Michal Jastrzebski",
    author_email='inc007@gmail.com',
    url='https://github.com/inc0/kolla_dockerhub_pusher',
    packages=[
        'kolla_dockerhub_pusher',
    ],
    package_dir={'kolla_dockerhub_pusher':
                 'kolla_dockerhub_pusher'},
    entry_points={
        'console_scripts': [
            'kolla_dockerhub_pusher=kolla_dockerhub_pusher.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='kolla_dockerhub_pusher',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
