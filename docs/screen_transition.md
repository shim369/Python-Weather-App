```mermaid
%%{init: {'flowchart': {'curve': 'linear'}}}%%

flowchart TD

    A[メイン画面]

    A --> B[都市名入力]
    B --> C[検索ボタン押下]
    C --> D[APIリクエスト]
    D --> E[レスポンス受信]
    E --> F[Weather生成]

    F --> G[結果表示]
    G --> A

    A --> H[検索履歴表示]
    H --> I[履歴一覧]
    I --> J[履歴詳細表示]
    J --> A

    A --> K[エラー表示]
    K --> A

    A --> L[アプリ終了]
