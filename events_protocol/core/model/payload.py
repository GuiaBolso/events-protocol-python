from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class RedirectPayload:
    url: str
    query_parameters: Dict[str, Any] = field(default={})
