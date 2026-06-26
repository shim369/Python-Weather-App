from weather_app.utils.logger import setup_logger
from weather_app.gui.app import WeatherApp


def main() -> None:
    setup_logger()
    # GUIクラスのインスタンス化
    app = WeatherApp()
    # 画面のメインループを開始
    app.mainloop()


if __name__ == "__main__":
    main()
