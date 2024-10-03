"""
daily_event_count.py
GHAでcronを回す際の指標を取得するため、connpassで1日に何件イベントが作成されているかを取得する
csvとして出力したらそれっぽく見れたりするかもしれない？
"""

import os
from typing import Optional
from dotenv import load_dotenv

import connpass_api
from datetime import datetime

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
    events = res["events"]

    summary:dict = dict()

    for event in events:
        updated: datetime = datetime.strptime(event["updated_at"], "%Y-%m-%dT%H:%M:%S%z")
        # dictに日付と時間ごとのイベント数を格納
        date_hour = updated.strftime("%Y-%m-%d %H:00")
        if date_hour in summary:
            summary[date_hour] += 1
        else:
            summary[date_hour] = 1
    
    # 日付ごとのイベント数を出力
    for date, count in summary.items():
        print(f"{date} : {count}件")