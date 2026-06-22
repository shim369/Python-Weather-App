from weather_app.gui.app import WeatherApp


def main() -> None:
    # GUIクラスのインスタンス化
    app = WeatherApp()
    # 画面のメインループを開始
    app.mainloop()


if __name__ == "__main__":
    main()
