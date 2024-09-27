import requests
import re
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os
import datetime

import json
from dotenv import load_dotenv


load_dotenv()

def search(channel, kwords):

    # 現在時刻を取得
    now = datetime.datetime.now()

    # 既存のリンクを取得
    existing_links = set()
    for item in root.findall(".//item/link"):
        existing_links.add(item.text)

    # connpass api呼び出し
    events = fetch_events()

    if events is None:
        return None
    
    for event in events:
        print(json.dumps(event, indent=4, ensure_ascii=False))

    return None

def fetch_events():
    url = os.environ.get("URL") + "/api/v1/event/"
    params = {"count":5,"order":3}
    headers = {"User-Agent": "curl/7.81.0"}
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        events = response.json()
        return events
    else:
        print(response)
        return None


if __name__ == "__main__":
    kwords = [
        "hokkaido",
        "aomori",
        "iwate",
        "miyagi",
        "akita",
        "yamagata",
        "fukushima",
        "ibaraki",
        "tochigi",
        "gunma",
        "saitama",
        "chiba",
        "tokyo",
        "kanagawa",
        "yamanashi",
        "niigata",
        "nagano",
        "toyama",
        "ishikawa",
        "fukui",
        "gifu",
        "shizuoka",
        "aichi",
        "mie",
        "shiga",
        "kyoto",
        "osaka",
        "nara",
        "hyogo",
        "wakayama",
        "shimane",
        "tottori",
        "okayama",
        "hiroshima",
        "yamaguchi",
        "tokushima",
        "kagawa",
        "ehime",
        "kochi",
        "fukuoka",
        "saga",
        "nagasaki",
        "kumamoto",
        "oita",
        "miyazaki",
        "kagoshima",
        "okinawa",
        "online",
    ]

    for kword in kwords:

        print (f"Searching for {kword} events...")
        # RSSファイルの読み込み
        output_file = f"./outputs/{kword}.xml"
        existing_links = set()
        if os.path.exists(output_file):
            tree = ET.parse(output_file)
            root = tree.getroot()
            for item in root.findall(".//item/link"):
                existing_links.add(item.text)
        else:
            root = ET.Element("rss", version="2.0")
            channel = ET.SubElement(root, "channel")
            title = "Connpassからのイベント情報"
            description = "Connpassからのイベント情報を提供します。"
            ET.SubElement(channel, "title").text = title
            ET.SubElement(channel, "description").text = description
            ET.SubElement(channel, "link").text = "https://niwanowa.github.io/makeRSSfromConnpass/"

        xml_pretty_str = search(root, kword)

        if xml_pretty_str is not None:
            with open(output_file, "w") as f:
                f.write(xml_pretty_str)
