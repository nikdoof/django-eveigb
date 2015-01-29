#!/usr/bin/env python
 
from setuptools import setup
from pip.req import parse_requirements
from eveigb import str_version

setup(name="django-eveigb",
      version=str_version,
      description="Django library/application for making use of EVE's In-Game Browser",
      author="Andrew Williams",
      author_email="andy@tensixtyone.com",
      url="https://github.com/nikdoof/django-eveigb",
      keywords="eveonline django igb",
      packages=['eveigb'],
      install_requires=['Django>=1.4,<1.7'],
      test_suite='test_project.tests.runtests',
)
