import json
import requests
from bs4 import BeautifulSoup

def fetch_telegram_posts(channel_name):
    url = f"https://t.me/s/{channel_name}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    posts = []
    messages = soup.find_all('div', class_='tgme_widget_message')
    
    for msg in messages:
        text_div = msg.find('div', class_='tgme_widget_message_text')
        time_tag = msg.find('time')
        
        if text_div:
            text = text_div.get_text(separator="\n").strip()
            date = time_tag.get('datetime', '') if time_tag else ''
            
            posts.append({
                "source": "Telegram",
                "text": text,
                "date": date,
                "link": f"https://t.me/{channel_name}"
            })
            
    return posts[-10:]  # Maxxansaalee 10 kanneen dhiyeenyaa

if __name__ == "__main__":
    print("Maxxansaalee fuutaa jira...")
    posts = fetch_telegram_posts("ayelebeharmee")
    
    with open("posts.json", "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
        
    print("Maxxansaaleen posts.json keessatti milkiidhaan saave ta'aniiru!")

