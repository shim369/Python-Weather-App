from weather_app.utils.logger import setup_logger
from weather_app.gui.app import WeatherApp
from weather_app.utils.logger import get_logger


logger = get_logger(__name__)


def main() -> None:
    setup_logger()
    # GUIクラスのインスタンス化
    app = WeatherApp()
    logger.info("Weather Appを起動しました。")
    # 画面のメインループを開始
    app.mainloop()


if __name__ == "__main__":
    main()
