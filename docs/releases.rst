Releases
========
Version 0.3.0
-------------
**Changed**

* ``aiohttp_things.views.PrimaryKeyMixin`` renamed to
  ``aiohttp_things.views.ItemMixin``.

**Added**

* Added ``aiohttp_things.views.PrimaryKeyMixin`` synonym for
  ``aiohttp_things.views.ItemMixin``.

Version 0.2.0
-------------
**Changed**

* Replace ``aiohttp.abc.AbstractView`` to ``aiohttp_things.views.ContextMixin``
  in parent classes of ``aiohttp_things.views.PrimaryKeyMixin``.
