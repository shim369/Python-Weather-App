from datetime import datetime
from zoneinfo import ZoneInfo
from weather_app.models.weather import Weather


def test_weather_object_creation():
    """Weatherモデルが正しく初期化され、属性が保持されるかテスト"""

    # テスト用のダミーデータを用意する
    dummy_time = datetime(2026, 6, 27, 10, 0, 0, tzinfo=ZoneInfo("Asia/Tokyo"))

    # 実際に Weather モデルのインスタンス（オブジェクト）を作る
    weather = Weather(
        city="Tokyo",
        temperature=25.5,
        description="clear sky",
        humidity=60,
        fetched_at=dummy_time
    )

    # 入れたデータが壊れずにそのまま取得できるか、assert でチェックする
    assert weather.city == "Tokyo"
    assert weather.temperature == 25.5
    assert weather.description == "clear sky"
    assert weather.humidity == 60
    assert weather.fetched_at == dummy_time

def test_weather_fetched_at_timezone():
    """fetched_at に正しいタイムゾーン（Asia/Tokyo）が設定されているかをテスト"""

    # 明示的に東京のタイムゾーンを持ったダミー時間を作る
    tokyo_tz = ZoneInfo("Asia/Tokyo")
    test_time = datetime(2026, 6, 27, 10, 0, 0, tzinfo=tokyo_tz)

    # Weatherモデルを作成
    weather = Weather(
        city="Osaka",
        temperature=28.0,
        description="rain",
        humidity=80,
        fetched_at=test_time
    )

    # タイムゾーンの正確性をアサートする
    # tzinfo が None（ネイブ）ではなく、正しく Asia/Tokyo になっているか？
    assert weather.fetched_at.tzinfo is not None
    assert weather.fetched_at.tzinfo.key == "Asia/Tokyo"

    # 時差（オフセット）が日本標準時の「+09:00」になっているか？
    assert weather.fetched_at.utcoffset().total_seconds() == 9 * 3600
