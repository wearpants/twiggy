####################
Tips And Tricks
####################

********************
Loggers
********************

.. _alternate-styles:

Alternate Styles
================
Old style works fine though:

>>> log.options(style='percent').info('I like %s', "bikes")
INFO:I like bikes

As do templates:

>>> log.options(style='dollar').info('$what kill', what='Cars')
INFO:Cars kill

.. _wsgi-support:

WSGI Extension
==============
OMG it don't exist yet.
