import sqlite3
from typing import Optional
from datetime import datetime
from weather_app.models.weather import Weather
from weather_app.utils.logger import get_logger
from weather_app.utils.decorators import time_logger, action_logger


logger = get_logger(__name__)

class WeatherRepository:

    def __init__(self, db_name: str = "weather.db", conn: Optional[sqlite3.Connection] = None) -> None:
        self.db_name = db_name
        # もし外から conn（接続）が渡されてきたらそれを使い、なければ None
        self._shared_conn = conn

    def _get_connection(self) -> sqlite3.Connection:
        # 共有された接続があればそれを返し、なければ毎回新しく開く
        if self._shared_conn:
            return self._shared_conn
        return sqlite3.connect(self.db_name)

    def create_table(self) -> None:
        conn = self._get_connection()
        cur = conn.cursor()
        cur.execute(
            'CREATE TABLE IF NOT EXISTS weather_history(id INTEGER PRIMARY KEY AUTOINCREMENT, city TEXT, temperature REAL, description TEXT, humidity INTEGER, fetched_at TEXT)')
        conn.commit()
        # もし共有接続（テスト環境）なら閉じず、通常（本番環境）なら閉じる
        if not self._shared_conn:
            conn.close()

    def save_history(self, weather: Weather) -> None:
        try:
            conn = self._get_connection()
            cur = conn.cursor()
            sql = 'INSERT INTO weather_history (city, temperature, description, humidity, fetched_at) VALUES (?, ?, ?, ?, ?)'
            values = (
                weather.city,
                weather.temperature,
                weather.description,
                weather.humidity,
                str(weather.fetched_at),
            )
            cur.execute(sql, values)
            conn.commit()
            logger.info("検索履歴を保存しました: %s", weather.city)
            cur.close()
            # もし共有接続（テスト環境）なら閉じず、通常（本番環境）なら閉じる
            if not self._shared_conn:
                conn.close()
        except sqlite3.Error as e:
            logger.error("データベースエラーが発生しました: %s", e)

    @action_logger
    @time_logger
    def get_all_history(self) -> list[Weather]:
        try:
            conn = self._get_connection()
            cur = conn.cursor()
            sql = 'SELECT * FROM weather_history ORDER BY fetched_at DESC'
            cur.execute(sql)
            rows =cur.fetchall()
            cur.close()
            # もし共有接続（テスト環境）なら閉じず、通常（本番環境）なら閉じる
            if not self._shared_conn:
                conn.close()

            histories = []
            for row in rows:
                # row[0]はid、row[1]はcity、row[2]はtemperature...
                weather_data = Weather(
                    city=row[1],
                    temperature=row[2],
                    description=row[3],
                    humidity=row[4],
                    fetched_at=datetime.fromisoformat(row[5]) # 文字列からdatetimeに戻すおまじない
                )
                histories.append(weather_data)

            return histories

        except sqlite3.Error as e:
            logger.error("データベースエラーが発生しました: %s", e)
            return []
