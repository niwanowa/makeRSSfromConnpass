import requests
import re
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os

def main(kwords):
    event_pattern = re.compile(r'<div class="event_list vevent">([\s\S]*?)<\/div>\s*<\/div>')
    
    output_file = "makeRSS_Connpass.xml"
    base_url = f"https://connpass.com/search/?start_from=2024%2F03%2F04&prefectures={kwords}&selectItem={kwords}&sort="
    url = base_url

    print(f"Starting with base URL: {base_url}")

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
        ET.SubElement(channel, "link").text = "https://example.com"

        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        html_content = response.text
        print(f"Response status code: {response.status_code}")
        
        events_found = 0
        channel = root.find("channel")
        
        found_events = event_pattern.findall(html_content)
        
        for match in found_events:
            event_html = match
            date = re.search(r'title="(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)"', event_html).group(1)
            title = re.search(r' alt="(.*?)" />', event_html).group(1)
            link = re.search(r'<p class="event_title"><a class="url summary" href="(https:\/\/[a-zA-Z0-9\-\.\/]+)"', event_html).group(1)

            print(f"Scraped Event: {title}, {link}")  # タイトルとリンクを出力
            
            if link in existing_links:
                continue
        
            # RSSのitem要素を追加
            new_item = ET.SubElement(channel, "item")
            ET.SubElement(new_item, "title").text = title
            ET.SubElement(new_item, "link").text = link
            ET.SubElement(new_item, "pubDate").text = date

    xml_str = ET.tostring(root)
    # 不正なXML文字を取り除く
    xml_str = re.sub(u'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', xml_str.decode()).encode()

    print("=== Debug: XML String Start ===")
    print(xml_str)
    print("=== Debug: XML String End ===")
    xml_pretty_str = minidom.parseString(xml_str).toprettyxml(indent="  ")
    xml_pretty_str = os.linesep.join([s for s in xml_pretty_str.splitlines() if s.strip()])
    
    with open(output_file, "w") as f:
        f.write(xml_pretty_str)

if __name__ == "__main__":
    kwords ="hokkaido"
    main(kwords)
