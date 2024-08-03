import os
import feedparser
from linebot import LineBotApi
from linebot.models import TextSendMessage

LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

def get_cnn_headlines():
    url = "http://rss.cnn.com/rss/edition.rss"
    feed = feedparser.parse(url)
    headlines = []
    for entry in feed.entries[:5]:  # Get top 5 headlines
        headlines.append({
            'title': entry.title,
            'url': entry.link
        })
    return headlines

def get_nhk_headlines():
    url = "https://www3.nhk.or.jp/rss/news/cat0.xml"
    feed = feedparser.parse(url)
    headlines = []
    for entry in feed.entries[:5]:  # Get top 5 headlines
        headlines.append({
            'title': entry.title,
            'url': entry.link
        })
    return headlines

def send_news():
    cnn_headlines = get_cnn_headlines()
    nhk_headlines = get_nhk_headlines()
    
    message = "Today's Headlines:\n\nCNN:\n"
    for headline in cnn_headlines:
        message += f"- {headline['title']} {headline['url']}\n"
    
    message += "\nNHK:\n"
    for headline in nhk_headlines:
        message += f"- {headline['title']} {headline['url']}\n"
    
    line_bot_api.broadcast(TextSendMessage(text=message))