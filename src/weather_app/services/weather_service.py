import httpx
import os
from dotenv import load_dotenv
from datetime import datetime
from weather_app.models.weather import Weather


load_dotenv()


class WeatherService:

    def fetch_weather(self, city: str) -> Weather:
        with httpx.Client() as client:
            url = "https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={API_key}"
            API_KEY = os.getenv("OPENWEATHER_API_KEY")

            if not API_KEY:
                raise RuntimeError(
                    "APIキーが設定されていません。` .env ` ファイルを確認してください。"
                )

            url = url.format(
                city_name=city, API_key=API_KEY
            )
            response = client.get(url)

            if response.status_code != 200:
                raise RuntimeError(
                    f"天気の取得に失敗しました (Status: {response.status_code})"
                )

            data = response.json()

            return Weather(
                city=data["name"],
                description=data["weather"][0]["description"],
                temperature=data["main"]["temp"],
                humidity=data["main"]["humidity"],
                fetched_at=datetime.now(),
            )
