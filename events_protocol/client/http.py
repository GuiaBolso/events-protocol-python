from typing import Dict

import requests
from requests.exceptions import ConnectTimeout, ReadTimeout, Timeout

from .exception.request_exception import (FailedDependencyException,
                                          TimeoutException)


class HttpClient:
    def post(self, url: str, headers: Dict[str, str], payload: str, timeout: int) -> str:
        try:
            response = requests.post(url=url, headers=headers, data=payload, timeout=timeout,)
        except (Timeout, ReadTimeout, ConnectTimeout) as exception:
            raise TimeoutException(f"Timeout calling {url}. Error {exception}")

        if not response.ok:
            raise FailedDependencyException(
                f"Failed dependency calling {url}. Error: {response.reason}"
            )

        return response.text
