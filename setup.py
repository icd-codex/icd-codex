#!/usr/bin/env python

"""The setup script."""

import sys
from setuptools import setup, find_packages

try:
    with open('./README.md') as readme_file, open('./HISTORY.md') as history_file:
        readme = readme_file.read()
        history = history_file.read()
except FileNotFoundError: # tox
    readme = history = ""

requirements = [
    'networkx',
    'node2vec',
    'untangle',
    'scikit-learn',
    'pandas',
    'requests'
]
if sys.version_info < (3,9):
    requirements.append("importlib-resources")
    
setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Jeremy Fisher",
    author_email='jeremy@adamsfisher.me',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
    ],
    description="graphical and continuous representations of ICD-9 and ICD-10 codes",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    package_data={"icdcodex.data": ["*"]},
    include_package_data=True,
    keywords='icdcodex',
    name='icdcodex',
    packages=find_packages(include=['icdcodex', 'icdcodex.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/icd-codex/icd-codex',
    version='0.5.1',
    zip_safe=True,
)
