import aiohttp_jinja2
import jinja2
import pytest
from aiohttp.web import Application

pytest_plugins = "aiohttp.pytest_plugin"


@pytest.fixture
def jinja2_application() -> Application:
    app = Application()
    aiohttp_jinja2.setup(
        app, enable_async=True, loader=jinja2.FileSystemLoader("tests/templates")
    )
    return app
