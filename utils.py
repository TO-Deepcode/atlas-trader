# Yardımcı fonksiyonlar (CryptoPanic entegrasyonu)
import requests
import os
from dotenv import load_dotenv

load_dotenv()
CRYPTOPANIC_KEY = os.getenv("CRYPTOPANIC_KEY")

def fetch_cryptopanic_news():
    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTOPANIC_KEY}&public=true"
    resp = requests.get(url)
    data = resp.json()
    news_list = []
    for item in data.get("results", []):
        news_list.append({
            "title": item.get("title"),
            "url": item.get("url"),
            "sentiment": item.get("vote"),
            "published_at": item.get("published_at")
        })
    return news_list
