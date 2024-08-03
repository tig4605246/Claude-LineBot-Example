import os
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, time
import pytz

from blueprints.line_webhook import line_webhook_bp
from blueprints.scheduled_tasks import scheduled_tasks_bp
from utils.news_service import send_news
from utils.stock_service import send_stock_prices

app = Flask(__name__)

# Register blueprints
app.register_blueprint(line_webhook_bp)
app.register_blueprint(scheduled_tasks_bp)

# Setup scheduler
scheduler = BackgroundScheduler(timezone=pytz.timezone('Asia/Taipei'))
scheduler.add_job(send_news, 'cron', hour=8, minute=30)
scheduler.add_job(send_stock_prices, 'cron', hour=12, minute=0)
scheduler.start()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)