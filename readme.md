# makeRSSfromconpass

## Description

connpass のイベント情報をスクレイピングして開催都道府県ごとの RSS を作成する

connpassのスクレイピング禁止化に伴いGHAでの自動作成を停止
connpassのAPI利用申請中 -> done

作成されたもの：
<https://niwanowa.github.io/makeRSSfromConnpass/hokkaido.xml>

## Usage

```bash
poetry install
poetry run python ./src/search.py
```
