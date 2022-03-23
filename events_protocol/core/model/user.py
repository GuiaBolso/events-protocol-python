from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    user_id: Optional[int]
    user_type: Optional[str]

    def __hash__(self):
        return hash(f"{self.user_id},{self.user_type}")

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()
