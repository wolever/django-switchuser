#!/usr/bin/env python

# NOTE: We need this little hack to make sure that tox will run correctly from
# a different directory (ex 'python ../django-switchuser/setup.py develop').
import os
os.chdir(os.path.dirname(__file__) or ".")

from setuptools import setup, find_packages

import django_switchuser

version = "%s.%s.%s" %django_switchuser.__version__
setup(
    name="django-switchuser",
    version=version,
    url="https://github.com/wolever/django-switchuser",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    license="BSD",
    classifiers=[ x.strip() for x in """
        Development Status :: 4 - Beta
        Intended Audience :: Developers
        Framework :: Django
        License :: OSI Approved :: BSD License
        Natural Language :: English
        Operating System :: OS Independent
        Programming Language :: Python
    """.split("\n") if x.strip() ],
)
