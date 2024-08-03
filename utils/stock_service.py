import os
import yfinance as yf
from linebot import LineBotApi
from linebot.models import TextSendMessage

LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

def get_stock_prices():
    # Define the stock symbols
    symbols = ['00929.TW', '0056.TW', '006208.TW']  # Use .TW suffix for Taiwan stocks
    
    prices = {}
    
    # Fetch the data for all symbols at once
    data = yf.download(symbols, period="1d")
    
    for symbol in symbols:
        try:
            # Get the latest closing price
            price = data['Close'][symbol].iloc[-1]
            prices[symbol] = f"{price:.2f}"
        except Exception as e:
            print(f"Error fetching stock price for {symbol}: {str(e)}")
            prices[symbol] = "Error"
    
    return prices

def send_stock_prices():
    stocks = get_stock_prices()
    message = "Current Stock Prices:\n"
    for symbol, price in stocks.items():
        message += f"{symbol}: {price}\n"
    
    line_bot_api.broadcast(TextSendMessage(text=message))