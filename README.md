Django-EVEIGB
=============

This library/application allows you to make use of EVE's in-game browser and most of the features available within it.

[![Build Status](https://travis-ci.org/nikdoof/django-eveigb.png?branch=master)](https://travis-ci.org/nikdoof/django-eveigb)

Installation
------------

1. Install the package with `setup.py`
2. Add `eveigb` to your `INSTALLED_APPS` in your `settings.py`
3. Add `eveigb.middleware.IGBMiddleware` to `MIDDLEWARE_CLASSES`
4. Add `eveigb.context_processors.igb` to `TEMPLATE_CONTEXT_PROCESSORS` if you wish to make use of the template variables


Usage
-----

The context processor makes a few variables available in your templates:

* `is_igb` - Indicates if the client is a EVE IGB client
* `is_igb_trusted` - Indicates if the client has trusted the site


Options
-------

* `EVEIGB_SECURE_HEADERS` - This will attempt to validate, as much as it can, the client as a IGB client.