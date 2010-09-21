######################
Configuration
######################

:data:`twiggy.emitters` is the root. Demo :function:`twiggy.addEmitters`

**********************
Emitter Objects
**********************

Emitters
========
filter + outputter

Filters
=======
take mesg, return bool. names, glob_names

Outputters
==========
paired with a formatter, do work of writing

Formatter
==========
<mumble>

.. _folding-exceptions:

You can fold exceptions by usin '\\n' as a prefix to fold into a single line.

***********************
Real config
***********************

Async Output
============
how it goes

Example configs
===============
a few

Log-level config
================
:attribute:`Logger.min_level` - for use by libraries - set to Levels.DISABLED.


Logger.filter, used to turn off stupidness


