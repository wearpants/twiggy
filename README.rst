Twiggy is a Pythonic logger.

.. code-block:: python
      
    >>> log.name('frank') \
    ...    .fields(number=42) \
    ...    .info('hello {who}, it's a {0} day',
                 'sunny',
                 who='world')
    INFO:frank:number=42:hello world, it's a sunny day

You should use Twiggy because it is awesome. For more information, read the `documentation <http://twiggy.wearpants.org>`_ or `see this blog post <http://blog.wearpants.org/meet-twiggy>`_.

Note that `master` is currently in flux and may be broken. Please use the `maint-0.4` branch for stable development/forks.
