#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("CHANGELOG.rst") as history_file:
    history = history_file.read()

# requirements = ['Click>=7.0', ]
requirements = list(map(str.strip, open("requirements.txt").readlines()))

setup_requirements = []

test_requirements = []

setup(
    author="Feite Brekeveld",
    author_email="f.brekeveld@gmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Virtual Finance API provides access to data from financial "
    "sites as if it was a REST-API.",
    entry_points={"console_scripts": ["vfapi=virtual_finance_api.cli:main"]},
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="virtual_finance_api",
    name="virtual_finance_api",
    packages=find_packages(include=["virtual_finance_api", "virtual_finance_api.*"]),
    setup_requires=requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/hootnot/virtual-finance-API",
    version="0.4.3",
    zip_safe=False,
)
