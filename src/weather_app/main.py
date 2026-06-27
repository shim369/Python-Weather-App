from weather_app.database.weather_repository import WeatherRepository
from weather_app.gui.app import WeatherApp
from weather_app.services.weather_service import WeatherService


def main() -> None:
    # 1. 本番用リポジトリの生成と初期化
    repository = WeatherRepository()
    repository.create_table()

    # 2. 天気サービスの生成
    service = WeatherService()

    # 3. アプリケーションの起動と「依存性の注入」
    # 画面クラスへ必要なパーツを引数として渡す
    app = WeatherApp(weather_service=service, weather_repository=repository)
    app.mainloop()


if __name__ == "__main__":
    main()
