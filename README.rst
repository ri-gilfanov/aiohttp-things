==============
aiohttp-things
==============
|ReadTheDocs| |PyPI release| |PyPI downloads| |License| |Python versions| |GitHub CI| |Codecov|

.. |ReadTheDocs| image:: https://readthedocs.org/projects/aiohttp-things/badge/?version=latest
  :target: https://aiohttp-things.readthedocs.io/en/latest/?badge=latest
  :alt: Read The Docs build

.. |PyPI release| image:: https://badge.fury.io/py/aiohttp-things.svg
  :target: https://pypi.org/project/aiohttp-things/
  :alt: Release

.. |PyPI downloads| image:: https://img.shields.io/pypi/dm/aiohttp-things
  :target: https://pypistats.org/packages/aiohttp-things
  :alt: PyPI downloads count

.. |License| image:: https://img.shields.io/badge/License-MIT-green
  :target: https://github.com/ri-gilfanov/aiohttp-things/blob/master/LICENSE
  :alt: MIT License

.. |Python versions| image:: https://img.shields.io/badge/Python-3.7%20%7C%203.8%20%7C%203.9-blue
  :target: https://pypi.org/project/aiohttp-things/
  :alt: Python version support

.. |GitHub CI| image:: https://github.com/ri-gilfanov/aiohttp-things/actions/workflows/ci.yml/badge.svg?branch=master
  :target: https://github.com/ri-gilfanov/aiohttp-things/actions/workflows/ci.yml
  :alt: GitHub continuous integration

.. |Codecov| image:: https://codecov.io/gh/ri-gilfanov/aiohttp-things/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/ri-gilfanov/aiohttp-things
  :alt: codecov.io status for master branch

Modest utility collection for development with `AIOHTTP
<https://docs.aiohttp.org/>`_ framework.

Documentation
-------------
https://aiohttp-things.readthedocs.io


Installation
------------
Installing ``aiohttp-things`` with pip: ::

  pip install aiohttp-things


Simple example
--------------
Example of AIOHTTP application
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: python

  import json
  import uuid
  from aiohttp import web
  from aiohttp_things.views import JSONMixin, PrimaryKeyMixin


  def safe_json_value(value):
      try:
          json.dumps(value)
          return value
      except (TypeError, OverflowError):
          return str(value)


  class Base(web.View, JSONMixin, PrimaryKeyMixin):
      async def get(self):
          self.context['Type of primary key'] = safe_json_value(type(self.pk))
          self.context['Value of primary key'] = safe_json_value(self.pk)
          return await self.finalize_response()


  class IntegerExample(Base):
      pk_adapter = int


  class UUIDExample(Base):
      pk_adapter = uuid.UUID


  UUID = '[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}'
  ROUTES = [
      web.view('/integer/{pk:[0-9]+}', IntegerExample),
      web.view(f'/uuid/{{pk:{UUID}}}', UUIDExample),
  ]


  async def app_factory():
      app = web.Application()
      app.add_routes(ROUTES)
      return app


  if __name__ == '__main__':
      web.run_app(app_factory())


Examples HTTP requests and response
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* \http://0.0.0.0:8080/integer/1

  .. code-block:: json

    {
      "Type of primary key": "<class 'int'>",
      "Value of primary key": 1
    }

* \http://0.0.0.0:8080/integer/9999999999999

  .. code-block:: json

    {
      "Type of primary key": "<class 'int'>",
      "Value of primary key": 9999999999999
    }

* \http://0.0.0.0:8080/integer/a352da04-c1af-4a44-8a94-c37f8f37b2bc
  ::

    404: Not Found

* \http://0.0.0.0:8080/integer/abc
  ::

    404: Not Found

* \http://0.0.0.0:8080/uuid/a352da04-c1af-4a44-8a94-c37f8f37b2bc

  .. code-block:: json

    {
      "Type of primary key": "<class 'uuid.UUID'>",
      "Value of primary key": "a352da04-c1af-4a44-8a94-c37f8f37b2bc"
    }

* \http://0.0.0.0:8080/uuid/13d1d0e0-4787-4feb-8684-b3da32609743

  .. code-block:: json

    {
      "Type of primary key": "<class 'uuid.UUID'>",
      "Value of primary key": "13d1d0e0-4787-4feb-8684-b3da32609743"
    }

* \http://0.0.0.0:8080/uuid/1
  ::

    404: Not Found

* \http://0.0.0.0:8080/uuid/abc
  ::

    404: Not Found
