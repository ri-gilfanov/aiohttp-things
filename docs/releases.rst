Releases
========
Version 0.6
-----------
**Changed**

* ``views.InstanceMixin`` and ``views.ListMixin`` inherited by 
  ``aiohttp.abc.AbstractView``;
* ``views.ItemMixin`` renamed to ``views.InstanceMixin``.

Version 0.5
-----------
**Removed**

* ``prepare_context()`` method removed from ``views.ContextMixin`` and
  ``views.ListMixin``.

Version 0.4
-----------
**Added**

** added ``views.Jinja2Mixin`` (need install ``aiohttp-jinja2``);
** added ``views.JSONMxixin``;
** added ``views.ListMixin``;

**Changed**

* ``views.PrimaryKeyMixin`` allocated in a separate mixin;
* ``views.ItemMixin`` inherited by ``views.ContextMixin`` and
  ``views.PrimaryKeyMixin``.

Version 0.3.0
-------------
**Changed**

* ``views.PrimaryKeyMixin`` renamed to
  ``views.ItemMixin``.

**Added**

* Added ``views.PrimaryKeyMixin`` synonym for ``views.ItemMixin``.

Version 0.2.0
-------------
**Changed**

* Replace ``aiohttp.abc.AbstractView`` to ``views.ContextMixin`` in parent
  classes of ``views.PrimaryKeyMixin``.
