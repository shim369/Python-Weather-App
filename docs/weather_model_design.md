# クラス設計

## Weather

役割：天気情報1件を表すエンティティ

責務：

* 天気情報を保持する
* 都市名、天気、気温、湿度、取得日時を管理する

使用技術：

* dataclass

---

## WeatherService

役割：天気情報取得

責務：

* OpenWeather APIへアクセスする
* 天気情報を取得する
* APIレスポンスをWeatherへ変換する
* 通信エラーを処理する

使用技術：

* httpx
* json

---

## WeatherRepository

役割：データ永続化

責務：

* 検索履歴保存
* 検索履歴取得
* 検索履歴削除
* SQLiteとのデータ連携

使用技術：

* sqlite3

---

## WeatherApp

役割：アプリケーション制御

責務：

* GUIイベントを管理する
* WeatherServiceを呼び出す
* WeatherRepositoryを呼び出す
* 取得結果を画面へ反映する

---

## GUI

役割：ユーザーとの対話

責務：

* 都市名入力
* 検索ボタン表示
* 天気情報表示
* エラーメッセージ表示
* 検索履歴表示

使用技術：

* Tkinter
