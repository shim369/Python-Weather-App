from typing import Any
from unittest.mock import patch
from weather_app.services.weather_service import WeatherService

@patch("weather_app.services.weather_service.httpx.get")
def test_fetch_weather_success(mock_get: Any) -> None:
    mock_get.return_value.json.return_value = {
        "name": "Tokyo",
        "weather": [{"description": "clear sky"}],
        "main": {
            "temp": 25.5,
            "humidity": 60
        }
    }

    # 1. 【実行】本物のサービスを作って、メソッドを呼び出す
    service = WeatherService()
    result = service.fetch_weather("Tokyo")

    # 2. 【検証】返ってきた result（Weatherオブジェクト）の中身をアサートする
    assert result.city == "Tokyo"
    assert result.temperature == 25.5
    assert result.description == "clear sky"
    assert result.humidity == 60
