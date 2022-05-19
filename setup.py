#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ 'SQLAlchemy>=1' ]

test_requirements = ['pytest>=3', ]

setup(
    author="Herman Singh",
    author_email='kartstig@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Extensions to SQLALchemy",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='sqlalchemy_extended',
    name='sqlalchemy_extended',
    packages=find_packages(include=['sqlalchemy_extended', 'sqlalchemy_extended.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/kartstig/sqlalchemy_extended',
    version='0.1.1',
    zip_safe=False,
)
