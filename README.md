# Fotoshi × 大阪 — SotM Asia 2026 振り返りマップ

[Fotoshi](https://fotoshi.com) の STAC API から大阪エリアで撮影された写真を取得し、[MapLibre GL JS](https://maplibre.org/) で地図上に表示する Web アプリです。State of the Map Asia 2026 振り返りハッカソンの作品です。

**公開ページ:** https://furuhashilab.github.io/Hackathon_Oct_Reara/

## 機能

- 大阪エリア（bbox: `135.3, 34.5, 135.7, 34.8`）の写真を地図上にマーカー表示
- 左サイドバーに写真一覧（サムネイル・撮影日時・投稿者・座標）
- 一覧の写真をクリックすると、その地点へ移動してポップアップを表示
- 地図上のマーカーをクリックすると、写真・撮影日時・投稿者・ライセンスをポップアップ表示（写真をクリックで高解像度版を開く）
- OpenStreetMap ベースのダークテーマ地図
- 写真（CC BY 4.0）と地図データ（© OpenStreetMap contributors）の帰属表示

## 使用技術

| 項目 | 内容 |
| --- | --- |
| 写真データ | [Fotoshi STAC API](https://fotoshi.com/developers)（`https://api.fotoshi.com/v1/stac`、コレクション `fotoshi-photos`） |
| 地図ライブラリ | MapLibre GL JS v4.7.1（cdnjs） |
| 背景地図 | OpenStreetMap 標準タイル（ラスタの明暗を反転してダーク化） |
| ホスティング | GitHub Pages |

## 構成

```
.
├── index.html              # Webアプリ本体（HTML/CSS/JS 1ファイル）
├── data/osaka.geojson      # Fotoshi STAC API から取得した大阪の写真データ（スナップショット）
├── scripts/fetch_osaka.py  # data/osaka.geojson を作り直すスクリプト
├── README.md
└── LICENSE                 # CC BY 4.0
```

### なぜデータを静的ファイルにしているか

Fotoshi STAC API の検索エンドポイント（`/v1/stac/search`）は API キーが必要で、CORS は `fotoshi.com` からのアクセスのみ許可されています。そのため GitHub Pages 上のブラウザから直接 API を呼ぶことはできません。

そこで、手元で API を呼んで結果を `data/osaka.geojson` に保存し、`index.html` はそのファイルを読み込む構成にしています。API キーをリポジトリに含めずに済むという利点もあります。

## データの更新方法

```bash
export FOTOSHI_STAC_API_KEY=fshi_xxxxxxxx   # https://fotoshi.com/account/developer で発行
python3 scripts/fetch_osaka.py
```

スクリプトは `GET /v1/stac/search?collections=fotoshi-photos&bbox=135.3,34.5,135.7,34.8&limit=100` を `next` リンクがなくなるまでたどり、表示に必要な項目だけを GeoJSON に保存します（API の制限: 1 キーあたり 30 リクエスト/分、1,000 件/日）。

## ローカルで動かす

`fetch()` で GeoJSON を読み込むため、ファイルを直接開くのではなくローカルサーバ経由で表示してください。

```bash
python3 -m http.server 8000
# → http://localhost:8000/ を開く
```

## ライセンス・帰属表示

- このリポジトリのコード・文章: © 2026 Reara Kato, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.ja)（[LICENSE](LICENSE)）
- 写真: 各投稿者 / [Fotoshi](https://fotoshi.com), CC BY 4.0
- 地図データ: © [OpenStreetMap contributors](https://www.openstreetmap.org/copyright)（ODbL）
