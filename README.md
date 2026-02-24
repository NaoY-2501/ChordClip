# ChordClip

キー・スケール・コードを選んで、コード音を MIDI ファイルとしてダウンロードできる Web アプリ

## 機能

- **キー選択**: C, C#, D など 12 キーから選択
- **スケール選択**: メジャー・スケール、ナチュラル・マイナー、ハーモニック・マイナー、教会旋法（アイオニアン、ドリアン、フリジアンなど）など多数のスケールに対応
- **BPM**: 60〜240 の範囲でテンポを指定
- **ルート音**: スケール上の音からルートを選択
- **コードタイプ**: maj, maj7, m7, triad, 7th, add9, sus2, sus4 から選択
- **MIDI ダウンロード**: 選択したコードの MIDI ファイル（`.mid`）を生成してダウンロード

## 必要環境

- Python 3.14 以上
- [uv](https://github.com/astral-sh/uv)（推奨）または pip

## セットアップ

```bash
# リポジトリをクローンしたあと、依存関係をインストール
uv sync
```

## 起動方法

プロジェクトルートで以下を実行

```bash
uv run streamlit run src/app.py
```

ブラウザが開き、`http://localhost:8501` で ChordClip が表示。

## プロジェクト構成

```
chordgen/
├── src/
│   ├── app.py          # Streamlit アプリ本体
│   ├── consts.py       # キー・コード定義、スケール CSV パス
│   ├── data/
│   │   └── scales.csv  # スケール定義（音程の半音オフセット）
│   ├── midi/
│   │   └── generate.py # MIDI ファイル生成
│   └── scraping/       # スケールデータ取得用（オプション）
├── pyproject.toml
└── README.md
```
