import json
import uuid

from aiohttp import web

import aiohttp_things as ahth


def safe_json_value(value):
    try:
        json.dumps(value)
    except (TypeError, OverflowError):
        return str(value)
    else:
        return value


class Base(web.View, ahth.JSONMixin, ahth.PrimaryKeyMixin):
    async def get(self):
        self.context["Type of primary key"] = safe_json_value(type(self.pk))
        self.context["Value of primary key"] = safe_json_value(self.pk)
        return await self.finalize_response()


class IntegerExample(Base):
    pk_adapter = int


class UUIDExample(Base):
    pk_adapter = uuid.UUID


UUID = "[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}"
ROUTES = [
    web.view("/integer/{pk:[0-9]+}", IntegerExample),
    web.view(f"/uuid/{{pk:{UUID}}}", UUIDExample),
]


async def app_factory():
    app = web.Application()
    app.add_routes(ROUTES)
    return app


if __name__ == "__main__":
    web.run_app(app_factory())
