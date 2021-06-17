from abc import ABCMeta
from typing import Any, Callable, Mapping

from aiohttp.abc import AbstractView
from aiohttp.web import Request


class ContextMixin(AbstractView, metaclass=ABCMeta):
    def __init__(self, request: Request) -> None:
        super().__init__(request)
        self.context: Mapping[str, Any] = {}


class PrimaryKeyMixin(AbstractView, metaclass=ABCMeta):
    pk_factory: Callable[..., Any] = str

    def __init__(self, request: Request) -> None:
        super().__init__(request)
        # Use regular expressions in routes for safe input
        self.pk = self.pk_factory(self.request.match_info.get('pk'))
