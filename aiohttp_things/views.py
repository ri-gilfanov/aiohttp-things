from abc import ABCMeta
from typing import Any, Callable, Mapping

from aiohttp.abc import AbstractView
from aiohttp.web import Request


class ContextMixin(AbstractView, metaclass=ABCMeta):
    """
    Class based view mixin with context attribute.
    """
    #: Dictionary for JSON response or HTML template response.
    context: Mapping[str, Any]

    def __init__(self, request: Request) -> None:
        super().__init__(request)
        self.context = {}


class PrimaryKeyMixin(ContextMixin, metaclass=ABCMeta):
    """
    Class based view mixin with primary key attribute.
    """
    #: Primary key from path variable for select an object from database.
    pk: Any

    #: Callable object for converting a primary key.
    pk_factory: Callable[..., Any] = lambda pk: pk

    def __init__(self, request: Request) -> None:
        super().__init__(request)
        # Use regular expressions in routes for safe input
        self.pk = self.pk_factory(self.request.match_info.get('pk'))
