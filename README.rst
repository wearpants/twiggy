Twiggy is a Pythonic logger.
      
>>> log.name('frank').fields(number=42).info("hello {who}, it's a {0} day", 'sunny', who='world')
INFO:frank:number=42:hello world, it's a sunny day

You should use Twiggy because it is awesome. For more information, `see this blog post <http://blog.wearpants.org/meet-twiggy>`_ or the `project homepage <http://twiggy.wearpants.org>`_.
