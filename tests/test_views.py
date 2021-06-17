import uuid

from aiohttp import web
from aiohttp.hdrs import METH_GET
from aiohttp.test_utils import make_mocked_request

from aiohttp_things.views import ContextMixin, PrimaryKeyMixin


def test_context_view() -> None:
    class ContextView(web.View, ContextMixin):
        pass

    req = make_mocked_request(METH_GET, '/')
    view = ContextView(req)
    assert isinstance(view.context, dict)


def test_integer_pk_view() -> None:
    class IntegerPrimaryKeyView(web.View, PrimaryKeyMixin):
        pk_factory = int

    pk = '1'
    req = make_mocked_request(METH_GET, f'/{pk}', match_info={'pk': pk})
    view = IntegerPrimaryKeyView(req)
    assert isinstance(view.pk, int)


def test_uuid_pk_view() -> None:
    class UUIDPrimaryKeyView(web.View, PrimaryKeyMixin):
        pk_factory = uuid.UUID

    pk = str(uuid.uuid4())
    req = make_mocked_request(METH_GET, f'/{pk}', match_info={'pk': pk})
    view = UUIDPrimaryKeyView(req)
    assert isinstance(view.pk, uuid.UUID)
