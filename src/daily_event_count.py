"""
daily_event_count.py
GHAでcronを回す際の指標を取得するため、connpassで1日に何件イベントが作成されているかを取得する
csvとして出力したらそれっぽく見れたりするかもしれない？
"""

import os
from typing import Optional
from dotenv import load_dotenv

import connpass_api
from datetime import datetime, timedelta
import csv
from zoneinfo import ZoneInfo

def output_csv(event_count: int, hour: str) -> None:
    """
    イベント数と時間をCSVファイルに追記します。

    この関数は、出力ディレクトリが存在しない場合に作成し、
    提供されたイベント数と時間を"outputs/event_count"ディレクトリ内の
    "event_count.csv"という名前のCSVファイルに追記します。CSVファイルが
    存在しない場合、ファイルを作成し、ヘッダー行を書き込みます。

    引数:
        hour (str): イベント数が記録された時間。
        event_count (int): 記録されたイベント数。

    例外:
        OSError: 出力ディレクトリの作成やCSVファイルへの書き込みに
                 問題がある場合に発生します。
    """
    # CSVファイルに追記
    output_dir: str = "outputs/event_count"
    csv_file_path: str = os.path.join(output_dir, "event_count.csv")

    file_exists: bool = os.path.isfile(csv_file_path)

    with open(csv_file_path, mode="a", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        if not file_exists:
            csv_writer.writerow(["datetime", "event_count"])
        csv_writer.writerow([event_count, hour])

if __name__ == "__main__":
    load_dotenv()

    # 環境変数から値を取得
    CONNPASS_HOST: Optional[str] = os.getenv("URL")

    if CONNPASS_HOST is None:
        raise ValueError("URL is not set")

    # connpass api呼び出し
    res: Optional[dict] = connpass_api.fetch_events(CONNPASS_HOST, order=1, count=100)

    if res is None:
        raise ValueError("Failed to fetch events from connpass API")

    # json形式のレスポンスからevents.eventsを取得
    events: list[dict[str, str]] = res["events"]

    summary: dict = dict()

    for event in events:
        updated: datetime = datetime.strptime(event["updated_at"], "%Y-%m-%dT%H:%M:%S%z")
        # dictに日付と時間ごとのイベント数を格納
        date_hour = updated.strftime("%Y-%m-%d %H:00")
        if date_hour in summary:
            summary[date_hour] += 1
        else:
            summary[date_hour] = 1

    # 日付と時間ごとのイベント数を出力
    for date_hour, count in summary.items():
        print(f"{date_hour} : {count}件")

    # 現在の日時を取得し、1時間前の日時を計算
    now = datetime.now(ZoneInfo("Asia/Tokyo"))
    two_hour_ago = now - timedelta(hours=2)
    two_hour_ago_str = two_hour_ago.strftime("%Y-%m-%d %H:00")

    # 2時間前のイベント件数を取得
    event_count = summary.get(two_hour_ago_str, 0)

    # CSVファイルに追記
    output_csv(event_count, two_hour_ago_str)