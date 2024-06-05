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
                bot.send_message(user_id, "Роутер доступний!")
            else:
                bot.send_message(user_id, "Роутер недоступний.")
            last_status = current_status
        time.sleep(15)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привіт! Введіть IP-адресу роутера.")

@bot.message_handler(func=lambda message: True)
def handle_ip_input(message):
    user_id = message.chat.id
    router_ip = message.text.strip()
    user_router[user_id] = router_ip
    threading.Thread(target=monitor_router, args=(user_id, router_ip)).start()

def main():
    bot.polling()

if __name__ == "__main__":
    main()
