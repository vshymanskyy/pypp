#!/usr/bin/env python

from setuptools import setup

setup(
    name         = "pypp",
    version      = "0.1.0",
    description  = "Python PreProcessor",
    platforms    = "any",
    url          = "https://github.com/vshymanskyy/pypp",
    license      = "MIT",
    author       = "Volodymyr Shymanskyy",
    author_email = "vshymanskyi@gmail.com",

    scripts      = ['bin/pypp'],
    py_modules   = ['pypp/pypp'],
    packages     = ['pypp/lang'],

    classifiers  = [
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X"
    ]
)
