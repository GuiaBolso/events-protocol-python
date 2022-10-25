import asyncio
import typing
from http import HTTPStatus

class BaseView:
    request = None

    _base_header = {"Content-Type": "application/json; charset=utf-8"}

    async def send_response(
        self,
        message: str = None,
        data: dict = None,
        description: str = None,
        http_status: int = None,
        code: int = 1000,
        log_level=None,
    ):

        http_status = int(http_status or HTTPStatus.OK)

        return await self.write_response(http_status=http_status, response_body=data)

    def get_query_args(self) -> typing.Dict[str, typing.Any]:
        raise NotImplementedError()

    async def write_response(
        self,
        http_status: int,
        description: str,
        response_body: dict,
        log_level: str = None,
        headers: dict = {},
    ):
        raise NotImplementedError()

    async def _treat_general_exception(self, exception: Exception) -> None:

        return await self.send_response(
            code=0, http_status=HTTPStatus.INTERNAL_SERVER_ERROR, description=str(exception),
        )


class BaseHealth(BaseView):

    _checkers: typing.List[
        typing.Dict[str, typing.Union[typing.Awaitable[typing.Callable], typing.Callable]]
    ] = []

    @classmethod
    def add_checker(
        cls,
        checker_name: str,
        checker_func: typing.Union[typing.Awaitable[typing.Callable], typing.Callable],
    ):
        cls._checkers.append({checker_name: checker_func})

    async def _get(self):
        try:
            CHECK_K = "checks"

            stats = {CHECK_K: []}
            for item in self._checkers:
                for key, func in item.items():
                    res = func()
                    if asyncio.iscoroutine(res):
                        res = await res
                    stats[CHECK_K] = stats[CHECK_K].append({key, res})
        except Exception as exc:
            stats = dict(error=str(exc))
        return await self.send_response(data=stats)
