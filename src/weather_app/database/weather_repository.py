import sqlite3
from datetime import datetime
from weather_app.models.weather import Weather


class WeatherRepository:

    def __init__(self, db_path: str = "weather.db") -> None:
        self.db_path = db_path
        self.create_table()

    def create_table(self) -> None:
        dbname = self.db_path
        conn = sqlite3.connect(dbname)
        # sqliteを操作するカーソルオブジェクトを作成
        cur = conn.cursor()
        cur.execute(
            'CREATE TABLE IF NOT EXISTS weather_history(id INTEGER PRIMARY KEY AUTOINCREMENT, city TEXT, temperature REAL, description TEXT, humidity INTEGER, fetched_at TEXT)')
        conn.commit()
        conn.close()

    def save_history(self, weather: Weather) -> None:
        dbname = self.db_path
        conn = sqlite3.connect(dbname)
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
        cur.close()
        conn.close()

    def get_all_history(self) -> list[Weather]:
        dbname = self.db_path
        conn = sqlite3.connect(dbname)
        cur = conn.cursor()
        sql = 'SELECT * FROM weather_history ORDER BY fetched_at DESC'
        cur.execute(sql)
        rows =cur.fetchall()
        cur.close()
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
