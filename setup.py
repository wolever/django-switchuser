#!/usr/bin/env python

# NOTE: We need this little hack to make sure that tox will run correctly from
# a different directory (ex 'python ../django-switchuser/setup.py develop').
import os
os.chdir(os.path.dirname(__file__) or ".")

from setuptools import setup, find_packages

import django_switchuser

version = "%s.%s.%s%s" %django_switchuser.__version__
setup(
    name="django-switchuser",
    version=version,
    packages=find_packages(),
    scripts=[
    ],
)
