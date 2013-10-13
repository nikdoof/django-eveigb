Django-EVEIGB
=============

This library/application allows you to make use of EVE's in-game browser and most of the features available within it.

[![wercker status](https://app.wercker.com/status/16ffeb1803105ce6f5c5209d67104211/m "wercker status")](https://app.wercker.com/project/bykey/16ffeb1803105ce6f5c5209d67104211)

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