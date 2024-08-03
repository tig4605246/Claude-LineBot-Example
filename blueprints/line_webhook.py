import os
from flask import Blueprint, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import google.generativeai as genai

from utils.news_service import get_cnn_headlines, get_nhk_headlines
from utils.stock_service import get_stock_prices

line_webhook_bp = Blueprint('line_webhook', __name__)

LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

@line_webhook_bp.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.lower()
    
    if user_message == 'news':
        cnn_headlines = get_cnn_headlines()
        nhk_headlines = get_nhk_headlines()
        
        message = "Latest Headlines:\n\nCNN:\n"
        for headline in cnn_headlines[:3]:
            message += f"- {headline['title']}\n"
        
        message += "\nNHK:\n"
        for headline in nhk_headlines[:3]:
            message += f"- {headline['title']}\n"
        
    elif user_message == 'stocks':
        stocks = get_stock_prices()
        message = "Current Stock Prices:\n"
        for symbol, price in stocks.items():
            message += f"{symbol}: {price}\n"
        
    else:
        # Use Gemini for other queries
        response = model.generate_content(user_message)
        message = response.text
    
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))