from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    user_id: Optional[int]
    query_parameters: Optional[str]
