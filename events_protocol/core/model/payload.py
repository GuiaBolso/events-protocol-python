from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class RedirectPayload:
    url: str
    query_parameters: Dict[str, Any] = field(default={})
