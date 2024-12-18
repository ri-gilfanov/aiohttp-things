import json
import uuid

import pytest
from aiohttp.hdrs import METH_GET, METH_POST
from aiohttp.test_utils import make_mocked_request
from aiohttp.web_app import Application
from aiohttp.web_exceptions import HTTPMethodNotAllowed
from aiohttp.web_response import StreamResponse, json_response
from aiohttp.web_urldispatcher import View

import aiohttp_things as ahth
from aiohttp_things import web_handlers


def test_context_view() -> None:
    class ContextView(View, ahth.ContextMixin):
        pass

    req = make_mocked_request(METH_GET, "/")
    view = ContextView(req)
    assert isinstance(view.context, dict)


async def test_http_method_view() -> None:
    class HTTPMethodView(ahth.HTTPMethodMixin):
        async def handle_request(self) -> StreamResponse:
            await super().handle_request()  # type: ignore

            return await (await self.determine_requested_method())()

    class GetMethodView(HTTPMethodView):
        async def get(self) -> StreamResponse:
            return json_response({"get_method": "success"})

    class PostMethodView(HTTPMethodView):
        async def post(self) -> StreamResponse:
            return json_response({"get_method": "success"})

    class GetAndPostMethodView(GetMethodView, PostMethodView):
        pass

    get_request = make_mocked_request(METH_GET, "/")
    post_request = make_mocked_request(METH_POST, "/")
    unkown_request = make_mocked_request("UNKNOWN", "/")

    get_method_view = GetMethodView(get_request)
    await get_method_view

    get_method_view = GetMethodView(post_request)
    with pytest.raises(HTTPMethodNotAllowed):
        await get_method_view

    post_method_view = PostMethodView(post_request)
    await post_method_view

    post_method_view = PostMethodView(get_request)
    with pytest.raises(HTTPMethodNotAllowed):
        await get_method_view

    get_and_post_method_view = GetAndPostMethodView(unkown_request)
    with pytest.raises(HTTPMethodNotAllowed):
        await get_and_post_method_view


def test_pagination_view() -> None:
    class PaginationView(View, ahth.PaginationMixin):
        page_key_adapter = int

    req = make_mocked_request(METH_GET, "/?page_key=2")
    view = PaginationView(req)
    assert isinstance(view.page_key, int)
    assert view.page_key == 2


def test_integer_pk_view() -> None:
    class IntegerPrimaryKeyView(View, ahth.PrimaryKeyMixin):
        pk_adapter = int

    pk = "1"
    req = make_mocked_request(METH_GET, f"/{pk}", match_info={"pk": pk})
    view = IntegerPrimaryKeyView(req)
    assert isinstance(view.pk, int)


def test_uuid_pk_view() -> None:
    class UUIDPrimaryKeyView(View, ahth.PrimaryKeyMixin):
        pk_adapter = uuid.UUID

    pk = str(uuid.uuid4())
    req = make_mocked_request(METH_GET, f"/{pk}", match_info={"pk": pk})
    view = UUIDPrimaryKeyView(req)
    assert isinstance(view.pk, uuid.UUID)


def test_item_mixin() -> None:
    class InstanceView(View, ahth.ItemMixin):
        pass

    req = make_mocked_request(METH_GET, "/")
    view = InstanceView(req)
    assert view.item is None
    view.item = 1
    assert view.item == 1


def test_list_mixin() -> None:
    class ListView(View, ahth.ListMixin):
        pass

    req = make_mocked_request(METH_GET, "/")
    view = ListView(req)
    item = "test_value"
    assert isinstance(view.items, list)
    view.items.append(item)
    assert item is view.items[0]


async def test_jinja2_mixin(jinja2_application: Application) -> None:
    class Jinja2View(View, ahth.Jinja2Mixin):
        template = "test.jinja2"

    app = jinja2_application
    req = make_mocked_request(METH_GET, "/", app=app)

    web_handlers.HAS_AIOHTTP_JINJA2 = False
    with pytest.raises(ImportError):
        view = Jinja2View(req)

    web_handlers.HAS_AIOHTTP_JINJA2 = True
    view = Jinja2View(req)
    resp = await view.finalize_response()
    assert isinstance(resp.body, bytes)
    assert resp.body == b"<h1>Test</h1>"


async def test_json_mixin() -> None:
    class JSONView(View, ahth.JSONMixin):
        pass

    req = make_mocked_request(METH_GET, "/")
    view = JSONView(req)
    data = {"numbers": [1, 2, 3]}
    view.context = data
    resp = await view.finalize_response()
    assert isinstance(resp.body, bytes)
    assert json.loads(resp.body) == data


async def test_response_format_mixin() -> None:
    class ResponseFormatView(View, ahth.ResponseFormatMixin):
        pass

    req = make_mocked_request(METH_GET, "/some", match_info={"format": ".html"})
    view = ResponseFormatView(req)
    assert view.response_format == ".html"

    req = make_mocked_request(
        METH_GET,
        "/some.json",
        match_info={"format": ".json"},
    )
    view = ResponseFormatView(req)
    assert view.response_format == ".json"


async def test_response_autoformat(jinja2_application: Application) -> None:
    class ResponseAutoformatView(View, ahth.ResponseAutoformatMixin):
        template = "test.jinja2"

    app = jinja2_application

    req = make_mocked_request(
        METH_GET,
        "/some",
        match_info={"format": ".html"},
        app=app,
    )
    view = ResponseAutoformatView(req)
    resp = await view.finalize_response()
    assert isinstance(resp.body, bytes)
    assert resp.body == b"<h1>Test</h1>"

    req = make_mocked_request(
        METH_GET,
        "/some.json",
        match_info={"format": ".json"},
    )
    view = ResponseAutoformatView(req)
    data = {"numbers": [1, 2, 3]}
    view.context = data
    resp = await view.finalize_response()
    assert isinstance(resp.body, bytes)
    assert json.loads(resp.body) == data
