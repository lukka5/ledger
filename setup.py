#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.rst", encoding="UTF-8") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst", encoding="UTF-8") as history_file:
    history = history_file.read()

requirements = [
    "pydantic>=1.8",
]

test_requirements = [
    "pytest>=3",
]

setup(
    author="Lucas Godoy",
    author_email="2lucasg@gmail.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description=(
        "Ledger - Keep track of financial transactions"
        " between different parties, people and organisations.",
    ),
    include_package_data=True,
    install_requires=requirements,
    keywords="ledger",
    license="MIT license",
    long_description=readme + "\n\n" + history,
    name="ledger",
    packages=find_packages(include=["ledger", "ledger.*"]),
    python_requires=">=3.6",
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/lukka5/ledger",
    version="0.1.0",
    zip_safe=False,
)
