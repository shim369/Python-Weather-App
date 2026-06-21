from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Weather:
    city: str
    description: str
    temperature: float
    humidity: int
    fetched_at: datetime
