#!/usr/bin/env python
from setuptools import setup, find_namespace_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    author="Stream Machine B.V.",
    author_email='apis@strmprivacy.io',
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    description="STRM Privacy Diagnostics for reporting privacy metrics on a dataset.",
    install_requires=[
        "pandas>=1.4.3",
        "numpy>=1.23.2",
        "matplotlib>=3.5.3",
        "fpdf>=1.7.2",
        "temp>=2020.7.2",
        "argparse>=1.4.0",
        "pathlib>=1.0.1",
        "seaborn>=0.11.2",
        "setuptools~=58.0.4",
        "scipy~=1.9.1"
    ],
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='strmprivacy privacy diagnostics',
    name='strmprivacy-diagnostics',
    packages=find_namespace_packages(include=['strmprivacy.*']),
    namespace_packages=["strmprivacy"],
    version='1.1.5',
    zip_safe=False,
)
