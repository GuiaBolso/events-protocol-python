import json
import tracemalloc
import typing
from http import HTTPStatus

from aiohttp.web import Application, Request, Response, View
from aiohttp.web_middlewares import _Middleware as AIOHTTPMiddleware

from events_protocol.core.views.base import BaseHealth, BaseView
from events_protocol.core.utils.encoder import JSONEncoder


async def init_app(
    routes: typing.List[typing.Tuple[View, str]],
    middlewares: typing.Iterable[AIOHTTPMiddleware] = [],
) -> Application:

    tracemalloc.start()
    app = Application(middlewares=middlewares)
    for view, path in routes:
        app.router.add_view(path, view)

    return app


_NOT_ALLOWED_AIOHTTP = Response(status=HTTPStatus.METHOD_NOT_ALLOWED)


class AIOHTTPView(BaseView, View):
    request: Request
    body: str = None

    def __init__(self, *args, **kwargs):
        self.request = args[0]
        super().__init__(*args, **kwargs)

    def __iter__(self):
        return self._iter().__await__()

    async def get_body(self):
        if not self.body and self.request.body_exists:
            _body: bytes = await self.request.content.read(-1)
            self.body = _body.decode("utf-8")
        return self.body

    async def get(self, *args, **kwargs):
        return await self._get(*args, **kwargs)

    async def _get(self, *args, **kwargs):
        return _NOT_ALLOWED_AIOHTTP

    async def put(self, *args, **kwargs):
        await self.get_body()
        return await self._put(*args, **kwargs)

    async def _put(self, *args, **kwargs):
        return _NOT_ALLOWED_AIOHTTP

    async def post(self, *args, **kwargs):
        await self.get_body()
        return await self._post(*args, **kwargs)

    async def _post(self, *args, **kwargs):
        return _NOT_ALLOWED_AIOHTTP

    async def delete(self, *args, **kwargs):
        return await self._delete(*args, **kwargs)

    async def _delete(self, *args, **kwargs):
        return _NOT_ALLOWED_AIOHTTP

    def get_query_args(self):
        return self.request.rel_url.query or dict()

    async def write_response(
        self, http_status: HTTPStatus, response_body: dict, headers: dict = {},
    ):
        headers.update(self._base_header)
        return Response(
            body=json.dumps(response_body, cls=JSONEncoder), status=http_status, headers=headers,
        )


class AIOHTTPHealthCheckView(BaseHealth, AIOHTTPView):
    pass
