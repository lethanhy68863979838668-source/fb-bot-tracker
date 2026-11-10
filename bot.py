import os
from threading import Thread
import time
from flask import Flask
import requests

TOKEN = "9218505324:AAH5dFo4fhmKYwRKY1ngmCUTIfquv8cbE"
CHAT_ID = "5340646272"
FILE_ID = "uids.txt"

app = Flask(__name__)


@app.route("/")
def home():
  return "Bot is running!"


def run_web():
  port = int(os.environ.get("PORT", 8080))
  app.run(host="0.0.0.0", port=port)


def run_bot():
  # Dán toàn bộ logic vòng lặp bot chính của bạn vào đây
  while True:
    try:
      # Code quét bot hiện tại của bạn
      time.sleep(5)
    except Exception as e:
      print(f"Lỗi: {e}")


if __name__ == "__main__":
  # Khởi động Web Server Flask ở luồng nền để giữ Railway luôn mở cổng
  web_thread = Thread(target=run_web)
  web_thread.daemon = True
  web_thread.start()

  # Chạy vòng lặp bot chính
  run_bot()﻿
