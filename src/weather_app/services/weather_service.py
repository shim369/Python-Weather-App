import httpx
import os
from dotenv import load_dotenv
from datetime import datetime
from zoneinfo import ZoneInfo
from weather_app.models.weather import Weather
from weather_app.utils.logger import get_logger


load_dotenv()
logger = get_logger(__name__)


class WeatherService:

    def fetch_weather(self, city: str) -> Weather:
        try:
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

                response.raise_for_status()

                data = response.json()

                tokyo_tz = ZoneInfo("Asia/Tokyo")

                return Weather(
                    city=data["name"],
                    description=data["weather"][0]["description"],
                    temperature=data["main"]["temp"],
                    humidity=data["main"]["humidity"],
                    fetched_at=datetime.now(tokyo_tz),
                )

        except httpx.HTTPStatusError as e:
            # ユーザーの入力ミス（404など）や一時的なAPIエラーは警告ログにする
            logger.warning(f"APIステータスエラーが発生しました: {e}")
            raise RuntimeError(f"都市が見つからないか、APIエラーが発生しました。({e.response.status_code})") from e

        except httpx.RequestError as e:
            # ネットワークが切れているなどの致命的な通信失敗はエラーログにする
            logger.error(f"ネットワーク通信に失敗しました: {e}")
            raise RuntimeError("天気情報の取得に失敗しました。ネット接続を確認してください。") from e
