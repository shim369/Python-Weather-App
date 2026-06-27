import pytest
import sqlite3
from datetime import datetime
from zoneinfo import ZoneInfo
from weather_app.models.weather import Weather
from weather_app.database.weather_repository import WeatherRepository

@pytest.fixture
def db_repo():
    # 1. 接続を1つだけ作る（これでメモリ上に1つの宇宙が固定される）
    conn = sqlite3.connect(":memory:")

    # 2. その接続をリポジトリに渡してインスタンス化する
    repo = WeatherRepository(conn=conn)

    repo.create_table()
    yield repo

    # 3. テストが終わったら接続を閉じる（ここで宇宙が消滅する）
    conn.close()

def test_save_and_get_history(db_repo):
    # この中では db_repo が自由に使える！

    tokyo_tz = ZoneInfo("Asia/Tokyo")
    test_time = datetime(2026, 6, 27, 10, 0, 0, tzinfo=tokyo_tz)
    dummy_weather = Weather(
        city="Osaka",
        temperature=28.0,
        description="rain",
        humidity=80,
        fetched_at=test_time
    )
    db_repo.save_history(dummy_weather)
    histories = db_repo.get_all_history()

    assert len(histories) == 1
    assert histories[0].city == "Osaka"
    assert histories[0].temperature == 28.0
