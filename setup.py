#!/usr/bin/env python
 
from distutils.core import setup

from eveigb import str_version
 
setup(name = "django-eveigb",
    version = str_version,
    description = "Django library/application for making use of EVE's In-Game Browser",
    author = "Andrew Williams",
    author_email = "matalok@pleaseignore.com",
    url = "https://github.com/nikdoof/django-eveigb",
    keywords = "eveonline django igb",
    packages = ['eveigb',],
)
