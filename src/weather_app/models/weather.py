from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Weather:
    city: str
    description: str
    temperature: float
    humidity: int
    fetched_at: datetime

    @staticmethod
    def celsius_to_fahrenheit(celsius: float) -> float:
        """
        doctest：摂氏を華氏に変換します。

        >>> Weather.celsius_to_fahrenheit(0.0)
        32.0
        """

        # 華氏へ変換
        fahrenheit = celsius * 1.8 + 32

        return fahrenheit
