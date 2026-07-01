import customtkinter as ctk
from weather_app.models.weather import Weather
from weather_app.services.weather_service import WeatherService
from weather_app.database.weather_repository import WeatherRepository

# テーマの設定
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class WeatherApp(ctk.CTk): # type: ignore[misc]

    def __init__(
        self,
        weather_service: WeatherService,
        weather_repository: WeatherRepository,
    ) -> None:
        """初期化メソッド。外からサービスとリポジトリを安全に注入する（Ch4, Ch5）"""
        super().__init__()

        # 注入されたインスタンスを保持
        self.weather_service = weather_service
        self.weather_repository = weather_repository

        self.title("Python Weather App")
        self.geometry("800x800")

        # ----------------------------------------------------
        # 1. 画面全体のグリッド（引き伸ばし）設定
        # ----------------------------------------------------
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=1)

        # ----------------------------------------------------
        # 2. 左側のフィールド（操作エリア / サイドバー）
        # ----------------------------------------------------
        left_frame = ctk.CTkFrame(master=self, width=220, corner_radius=10)
        left_frame.grid(row=0, column=0, padx=(10, 5), pady=(10, 5), sticky="nsew")
        left_frame.grid_propagate(False)

        label_title = ctk.CTkLabel(
            master=left_frame, text="天気検索", font=ctk.CTkFont(size=14, weight="bold")
        )
        label_title.pack(padx=20, pady=15)

        self.entry = ctk.CTkEntry(
            master=left_frame, placeholder_text="都市名を入力...", width=160
        )
        self.entry.pack(padx=20, pady=10)

        button = ctk.CTkButton(
            master=left_frame,
            text="検索",
            command=self._on_search_clicked,
            width=160,
        )
        button.pack(padx=20, pady=10)

        # ----------------------------------------------------
        # 3. 右側のフィールド（結果表示エリア / メイン）
        # ----------------------------------------------------
        right_frame = ctk.CTkFrame(master=self, corner_radius=10)
        right_frame.grid(row=0, column=1, padx=(5, 10), pady=(10, 5), sticky="nsew")

        label_right_title = ctk.CTkLabel(
            master=right_frame, text="検索結果", font=ctk.CTkFont(size=14, weight="bold")
        )
        label_right_title.pack(padx=20, pady=15)

        self.result_label = ctk.CTkLabel(
            master=right_frame,
            text="ここに結果が表示されます",
            font=ctk.CTkFont(size=14, weight="normal"),
            justify="left",
        )
        self.result_label.pack(pady=40, padx=20)

        # ----------------------------------------------------
        # 4. 一番下のフィールド（履歴表示エリア）
        # ----------------------------------------------------
        history_frame = ctk.CTkScrollableFrame(master=self, corner_radius=10)
        history_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=(5, 10), sticky="nsew")

        history_title = ctk.CTkLabel(
            master=history_frame,
            text="検索履歴",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        history_title.pack(fill="x", padx=10, pady=(5, 10))

        self.history_label = ctk.CTkLabel(
            master=history_frame,
            text="まだ履歴はありません",
            font=ctk.CTkFont(size=13, weight="normal"),
            justify="left",
            anchor="w"
        )
        self.history_label.pack(fill="x", padx=10, pady=(5, 10))

        # その都度生成せず、注入された self.weather_repository から取得
        self._refresh_history_display()

    def _refresh_history_display(self) -> None:
        """データベースから最新の履歴を読み込んで画面に反映する内部メソッド"""
        histories = self.weather_repository.get_all_history()

        if not histories:
            self.history_label.configure(text="まだ履歴はありません")
        else:
            history_text = "".join(
                f"[{weather.fetched_at:%H:%M:%S}] "
                f"{weather.city}: {weather.temperature}℃\n"
                for weather in histories
            )
            self.history_label.configure(text=history_text)

    def _on_search_clicked(self) -> None:
        """検索ボタンが押された時の処理（ビジネスロジックの呼び出し）"""
        try:
            input_city = self.entry.get().strip() or "未入力"

            # 注入されたインスタンスを使ってAPI取得と保存を行う
            result = self.weather_service.fetch_weather(input_city)
            self.weather_repository.save_history(result)

            fahrenheit_val = Weather.celsius_to_fahrenheit(result.temperature)

            # 検索結果の更新
            display_text = (
                f"検索した都市: {input_city}\n\n"
                f"都市: {result.city}\n"
                f"天気: {result.description}\n"
                f"気温: {result.temperature}℃ ({fahrenheit_val:.1f}℉)\n"
                f"湿度: {result.humidity}%"
            )
            self.result_label.configure(text=display_text)

            # 履歴表示の更新（DBの最新状態から再描画する形に洗練）
            self._refresh_history_display()

        except RuntimeError as e:
            error_text = f"エラーが発生しました\n\n{e}\n\n都市名が正しいか確認してください。"
            self.result_label.configure(text=error_text)
