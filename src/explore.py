import requests
import re
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os
import datetime


def explore(channel, kwords):
    event_pattern = re.compile(r'<div class="recent_event_list">([\s\S]*?)<\/div>\s*<\/div>')

    base_url = "http://connpass.com/explore/"
    url = base_url
    include_words = kwords

    # 既存のリンクを取得
    existing_links = set()
    for item in root.findall(".//item/link"):
        existing_links.add(item.text)

    print(f"Starting with base URL: {base_url}")

    for page in range(1, 10):
        print(f"Fetching page {page}...")
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        html_content = response.text
        print(f"Response status code: {response.status_code}")

        events_found = 0
        channel = root.find("channel")

        found_events = event_pattern.findall(html_content)
        print(f"Found {len(found_events)} events on page {page}.")

        for match in found_events[::-1]:
            event_html = match
            date = re.search(r'title="(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)"', event_html).group(1)
            date = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
            # timezoneをUTCからJSTに変換
            date = date.replace(tzinfo=datetime.timezone.utc)
            date = date.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
            title_link = re.search(
                r'<a class="image_link event_thumb" href="(https:\/\/[a-zA-Z0-9\-\.\/]+)" title="(.*?)">', event_html
            )
            link, title = title_link.groups()

            print(f"Scraped Event: {title}, {link}, {date}")  # タイトルとリンクを出力

            # すでにRSSに存在するリンクの場合はスキップ
            if link in existing_links:
                continue

            if any(word in title for word in include_words):
                new_item = ET.SubElement(channel, "item")
                ET.SubElement(new_item, "title").text = title
                ET.SubElement(new_item, "link").text = link
                ET.SubElement(new_item, "pubDate").text = date

        print(f"Found {events_found} events on page {page}.")

        next_page = re.search(r'<a href="\?page=(\d+)">次へ&gt;&gt;<\/a>', html_content)

        if next_page:
            url = base_url + "?page=" + next_page.group(1)
        else:
            print("No more pages found.")
            break

    xml_str = ET.tostring(root)
    # 不正なXML文字を取り除く
    xml_str = re.sub("[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", xml_str.decode()).encode()
    xml_pretty_str = minidom.parseString(xml_str).toprettyxml(indent="  ")
    xml_pretty_str = os.linesep.join([s for s in xml_pretty_str.splitlines() if s.strip()])

    return xml_pretty_str


if __name__ == "__main__":
    kwords = ["Hokkaido", "北海道"]
    output_file = f"explore_{kwords}.xml"

    if os.path.exists(output_file):
        tree = ET.parse(output_file)
        root = tree.getroot()
    else:
        root = ET.Element("rss", version="2.0")
        channel = ET.SubElement(root, "channel")
        title = "Connpassからのイベント情報"
        description = "Connpassからのイベント情報を提供します。"
        ET.SubElement(channel, "title").text = title
        ET.SubElement(channel, "description").text = description
        ET.SubElement(channel, "link").text = "https://example.com"

    xml_pretty_str = explore(root, kwords)

    with open(output_file, "w") as f:
        f.write(xml_pretty_str)
