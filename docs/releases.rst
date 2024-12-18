Releases
========
Version 1.1.0
-------------
**Changed**

* Update dependencies.

**Removed**

* Dropped support for Python 3.8;
* Removed `page` and `page_adapter` attributes (deprecated in v0.14) from `PaginationMixin` class.

Version 1.0.1
-------------

**Added**

* Added support for Python 3.13.

**Changed**

* Update dependencies.

Version 1.0.0
-------------

**Added**

* Added support for Python 3.11 and 3.12.

**Removed**

* Dropped support for Python 3.7.

Version 0.14
------------
**Added**

* Added Python 3.11 and 3.12 support;
* Added ``page_key_adapter`` attribute instead ``page_adapter`` attribute.

**Deprecated**

* ``page`` attribute is deprecated. Use `page_key`` attribute;
* ``page_adapter`` is deprecated. Use ``page_key_adapter`` attribute.

Version 0.14
------------
**Added**

* Added ``page_key`` attribute instead ``page`` attribute;
* Added ``page_key_adapter`` attribute instead ``page_adapter`` attribute.

**Deprecated**

* ``page`` attribute is deprecated. Use `page_key`` attribute;
* ``page_adapter`` is deprecated. Use ``page_key_adapter`` attribute.

Version 0.13
------------
**Added**

* ``paginator`` attribute to ``PaginationMixin``.

Version 0.12
------------
**Added**

* ``ResponseAutoformatMixin``.

**Changed**

* Renamed ``handlers`` module to ``web_handlers``.

Version 0.11
------------
**Added**

* ``HTTPMethodMixin``.

**Removed**

* ``finalize_response`` method in ``AbstractHandler``.

Version 0.10
------------
**Added**

* ``AbstractHandler``.

**Changed**

* ``views`` module renamed to ``handlers``;
* classes from ``handlers`` temporarily imported to empty ``views`` module for
  backward compatibility.

**Removed**

** ``InstanceMixin`` a synonym for ``ItemMixin``.

Version 0.9
-----------
**Added**

* Added ``views.PaginationMixin``;
* Added ``ContextMixin``, ``ItemMixin``, ``Jinja2Mixin``, ``JSONMixin``,
  ``ListMixin``, ``PaginationMixin``, ``PrimaryKeyMixin`` to package namespace.

**Removed**

* ``instance`` attribute removed from ``ItemMixin``, use ``ItemMixin.item``;
* ``pk_factory`` attribute removed from ``PrimaryKeyMixin``, use
  ``PrimaryKeyMixin.pk_adapter``.

Version 0.8
-----------
**Added**
* ``ResponseFormatMixin``

**Changed**
* ``views.InstanceMixin`` class renamed to ``views.ItemMixin``;
* ``views.ItemMixin`` synonym renamed to ``views.InstanceMixin``.

Version 0.7
-----------
**Add**

* ``views.PrimaryKeyMixin.pk_adapter`` instead ``views.PrimaryKeyMixin.pk_factory``.

**Deprecated**

* ``views.PrimaryKeyMixin.pk_factory``.

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
