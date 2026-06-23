from datetime import datetime
import customtkinter as ctk
from weather_app.services.weather_service import WeatherService

# テーマの設定
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class WeatherApp(ctk.CTk):

    def __init__(self) -> None:
        super().__init__()
        self.title("Python Weather App")
        self.geometry("600x600")  # 縦幅を履歴表示用に少し広げました

        # ----------------------------------------------------
        # 1. 画面全体のグリッド（引き伸ばし）設定
        # ----------------------------------------------------
        self.grid_columnconfigure(1, weight=1)  # 右側列を自動で広げる
        self.grid_rowconfigure(0, weight=2)     # 上段（検索・結果）の伸びる比率
        self.grid_rowconfigure(1, weight=1)     # 下段（履歴）の伸びる比率

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
        # 💡 label_text="検索履歴" を削除して、ただのスクロールフレームにする
        history_frame = ctk.CTkScrollableFrame(master=self, corner_radius=10)
        history_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=(5, 10), sticky="nsew")

        # 👑 タイトル専用のラベルを「太字（bold）」で作成して一番上に追加
        history_title = ctk.CTkLabel(
            master=history_frame,
            text="検索履歴",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        history_title.pack(fill="x", padx=10, pady=(5, 10))

        # 📄 履歴のテキスト（中身）を表示するラベル（こっちは通常の太さ）
        self.history_label = ctk.CTkLabel(
            master=history_frame,
            text="まだ履歴はありません\n",
            font=ctk.CTkFont(size=13, weight="normal"),
            justify="left",
            anchor="w"
        )
        self.history_label.pack(fill="x", padx=10, pady=(5, 10))

    def _on_search_clicked(self) -> None:
        input_city = self.entry.get() if self.entry.get() else "未入力"

        result = WeatherService().fetch_weather(input_city)
        # 検索結果の更新
        display_text = (
            f"検索した都市: {input_city}\n\n"
            f"都市: {result.city}\n"
            f"天気: {result.description}\n"
            f"気温: {result.temperature}℃\n"
            f"湿度: {result.humidity}%"
        )
        self.result_label.configure(text=display_text)

        # 履歴表示の更新（新規の検索履歴を上に追加していく）
        current_time = datetime.now().strftime("%H:%M:%S")
        new_history = f"[{current_time}] {input_city} の天気を検索しました\n"

        # 既存の履歴テキストを取得して、新しい履歴を先頭に結合
        old_history = self.history_label.cget("text")
        if old_history == "まだ履歴はありません\n":
            old_history = ""
        self.history_label.configure(text=new_history + old_history)
