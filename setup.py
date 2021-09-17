#!/usr/bin/env python

"""The setup script."""
from glob import glob
from os.path import basename, dirname, join, splitext

from setuptools import find_packages, setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ["pygame"]

setup_requirements = ['pytest-runner']

test_requirements = ['pytest']

with open('requirements_dev.txt', 'r') as f:
    dev_requirements = [l for l in f.read().split('\n') if l.strip()]
dev_requirements += requirements

setup(
    name='yammy',
    author="Ivan Ogasawara",
    author_email='ivan.ogasawara@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Python Game Engine",
    install_requires=requirements,
    extras_require={'dev': dev_requirements},
    license="BSD license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='yammy',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    # py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/xmnlab/yammy',
    version='0.1.0',
    zip_safe=False,
)
