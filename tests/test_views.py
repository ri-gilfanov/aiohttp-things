import json
import uuid

import aiohttp_jinja2
import jinja2
import pytest
from aiohttp import web
from aiohttp.hdrs import METH_GET
from aiohttp.test_utils import make_mocked_request

from aiohttp_things import views
from aiohttp_things.views import (
    ContextMixin,
    InstanceMixin,
    Jinja2Mixin,
    JSONMixin,
    ListMixin,
    PrimaryKeyMixin,
)


def test_context_view() -> None:
    class ContextView(web.View, ContextMixin):
        pass

    req = make_mocked_request(METH_GET, '/')
    view = ContextView(req)
    assert isinstance(view.context, dict)


def test_integer_pk_view_deprecated() -> None:
    class IntegerPrimaryKeyView(web.View, PrimaryKeyMixin):
        pk_factory = int

    pk = '1'
    req = make_mocked_request(METH_GET, f'/{pk}', match_info={'pk': pk})
    view = IntegerPrimaryKeyView(req)
    assert isinstance(view.pk, int)


def test_uuid_pk_view_deprecated() -> None:
    class UUIDPrimaryKeyView(web.View, PrimaryKeyMixin):
        pk_factory = uuid.UUID

    pk = str(uuid.uuid4())
    req = make_mocked_request(METH_GET, f'/{pk}', match_info={'pk': pk})
    view = UUIDPrimaryKeyView(req)
    assert isinstance(view.pk, uuid.UUID)


def test_integer_pk_view() -> None:
    class IntegerPrimaryKeyView(web.View, PrimaryKeyMixin):
        pk_adapter = int

    pk = '1'
    req = make_mocked_request(METH_GET, f'/{pk}', match_info={'pk': pk})
    view = IntegerPrimaryKeyView(req)
    assert isinstance(view.pk, int)


def test_uuid_pk_view() -> None:
    class UUIDPrimaryKeyView(web.View, PrimaryKeyMixin):
        pk_adapter = uuid.UUID

    pk = str(uuid.uuid4())
    req = make_mocked_request(METH_GET, f'/{pk}', match_info={'pk': pk})
    view = UUIDPrimaryKeyView(req)
    assert isinstance(view.pk, uuid.UUID)


def test_instance_mixin() -> None:
    class InstanceView(web.View, InstanceMixin):
        pass

    req = make_mocked_request(METH_GET, '/')
    view = InstanceView(req)
    assert view.instance is None
    view.instance = 1
    assert view.instance == 1


def test_list_mixin() -> None:
    class ListView(web.View, ListMixin):
        pass

    req = make_mocked_request(METH_GET, '/')
    view = ListView(req)
    item = 'test_value'
    assert isinstance(view.items, list)
    view.items.append(item)
    assert item is view.items[0]


async def test_jinja2_mixin() -> None:
    class Jinja2View(web.View, Jinja2Mixin):
        template = 'test.jinja2'

    app = web.Application()
    aiohttp_jinja2.setup(
        app,
        enable_async=True,
        loader=jinja2.FileSystemLoader('tests/templates')
    )
    req = make_mocked_request(METH_GET, '/', app=app)

    views.HAS_AIOHTTP_JINJA2 = False
    with pytest.raises(ImportError):
        view = Jinja2View(req)

    views.HAS_AIOHTTP_JINJA2 = True
    view = Jinja2View(req)
    resp = await view.finalize_response()
    assert isinstance(resp.body, bytes)
    assert resp.body == b'<h1>Test</h1>'


async def test_json_mixin() -> None:
    class JSONView(web.View, JSONMixin):
        pass

    req = make_mocked_request(METH_GET, '/')
    view = JSONView(req)
    data = {'numbers': [1, 2, 3]}
    view.context = data
    resp = await view.finalize_response()
    assert isinstance(resp.body, bytes)
    assert json.loads(resp.body) == data
