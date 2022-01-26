from dataclasses import dataclass
from typing import Optional


@dataclass
class Identity:
    user_id: Optional[int]
    query_parameters: Optional[str]
