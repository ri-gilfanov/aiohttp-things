import json
import uuid
from aiohttp import web
from aiohttp_things.views import ContextMixin, PrimaryKeyMixin


def safe_json_value(value):
    try:
        json.dumps(value)
        return value
    except (TypeError, OverflowError):
        return str(value)


class Base(web.View, ContextMixin, PrimaryKeyMixin):
    async def get(self):
        pk_type = type(self.pk)
        self.context['Type of primary key'] = safe_json_value(pk_type)
        self.context['Value of primary key'] = safe_json_value(self.pk)
        return web.json_response(self.context)


class IntegerExample(Base):
    pk_factory = int


class UUIDExample(Base):
    pk_factory = uuid.UUID


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
