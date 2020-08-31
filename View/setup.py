"""
Created on Mon Aug 31 17:31:58 2020

Contains setup information for the package.
"""

import setuptools
import os

with open(os.path.realpath("..") + "README.md", "r") as file:
    long_description = file.read()

setuptools.setup(
    name="BasicTwitterView",
    version="0.0.1",
    author="Brian Sun",
    author_email="briansunela@gmail.com",
    description="Contains view elements of the Basic Twitter app.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bsun94/simpletwitter",
    packages=setuptools.find_packages(),
    classifiers=["Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"],
    python_requires=">=3.6"
    )