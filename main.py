import os
from dotenv import load_dotenv
import telebot
import requests
import time
import threading

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

requests.packages.urllib3.disable_warnings()

bot = telebot.TeleBot(TELEGRAM_TOKEN)

user_router = {}

def check_router(ip_address):
    url = f"https://{ip_address}:8443"
    try:
        response = requests.get(url, verify=False, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def monitor_router(user_id, ip_address):
    last_status = None
    while True:
        current_status = check_router(ip_address)
        if current_status != last_status:
            if current_status:
                bot.send_message(user_id, "Світло є 💡")
            else:
                bot.send_message(user_id, "Світла немає 🕯️")
            last_status = current_status
        time.sleep(60)

def handler(event, context):
    try:
        update = telebot.types.Update.de_json(event["body"])
        bot.process_new_updates([update])
        return {
            "statusCode": 200,
            "body": "",
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e),
        }

if __name__ == "__main__":
    main()
