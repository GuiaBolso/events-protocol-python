from uuid import UUID
from dataclasses import dataclass


@dataclass
class EventContext:
    id: UUID
    flow_id: UUID
