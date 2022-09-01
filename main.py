import requests
from dotenv import load_dotenv
import os
import time


def send_msg(text):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    print(f"Sending message: {text}")
    url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text
    requests.get(url_req, timeout=10)


def get_enrollers():
    enrollers_client = requests.get(
        "https://www.udemy.com/api-2.0/instructor-performance/enrollment-metrics/?fields[user]=total,current_month,daily,monthly",
        cookies=cookies, timeout=10)
    return enrollers_client.json()["results"][0]["total"]

def get_earned():
    earned_client = requests.get(
        "https://www.udemy.com/api-2.0/share-holders/v1.0/371956/total/?timeframe=month&aggregate=day&breakdown=revenue_type",
        cookies=cookies, timeout=10)
    return earned_client.json()["amount"]["amount"]


load_dotenv()

cookies = {
    "access_token": os.getenv("ACCESS_TOKEN"),
}

starttime = time.time()

actual_enrollers = 0
actual_earned = 0

while True:
    enrollers = get_enrollers()
    if actual_enrollers != enrollers:
        actual_enrollers = enrollers
        send_msg(f"🙋 Nuovo studente, ora: {enrollers} studenti")

    earned = get_earned()
    if actual_earned != earned:
        actual_earned = earned
        send_msg(f"🤑 Nuove entrate, ora: {earned}$")

    time.sleep(600.0 - ((time.time() - starttime) % 600.0))
