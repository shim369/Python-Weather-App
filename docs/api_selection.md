# API選定書

## API名

OpenWeather

## 用途

現在の天気情報取得

## 通信方式

HTTPS

## レスポンス形式

JSON

## 認証

API Key

## 利用ライブラリ

httpx

## 利用エンドポイント

Current Weather Data API

## 選定理由

- 無料プランが利用可能
- Pythonでの利用事例が豊富
- JSONレスポンスが分かりやすい
- HTTP通信（httpx）の学習に適している
- dataclassによるモデル化の練習ができる
- datetimeによる日時処理の学習に適している
- pytest・mockによるテストが行いやすい

## 本プロジェクトで利用する主なデータ

- 都市名
- 天気概要
- 気温
- 湿度
- 取得日時
