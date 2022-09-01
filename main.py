import requests
from dotenv import load_dotenv
import os
from threading import Timer
import redis


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
    json = enrollers_client.json()
    if "results" in json:
        return json["results"][0]["total"]
    else:
        return None


def get_earned():
    earned_client = requests.get(
        "https://www.udemy.com/api-2.0/share-holders/v1.0/371956/total/?timeframe=month&aggregate=day&breakdown=revenue_type",
        cookies=cookies, timeout=10)
    json = earned_client.json()
    if "amount" in json:
        return earned_client.json()["amount"]["amount"]
    else:
        return None


def check():
    global actual_enrollers, actual_earned, problems_notice

    enrollers = get_enrollers()
    if enrollers is not None:
        if actual_enrollers != enrollers:
            problems_notice = False
            actual_enrollers = enrollers
            redis.set("enrollers", enrollers)
            send_msg(f"🙋 Nuovo studente, ora: {enrollers} studenti")
    elif not problems_notice:
        send_msg("Problems with APIs")
        problems_notice = True

    earned = get_earned()
    if earned is not None:
        if actual_earned != earned:
            problems_notice = False
            actual_earned = earned
            redis.set("earned", earned)
            send_msg(f"🤑 Nuove entrate, ora: {earned}$")
    elif not problems_notice:
        send_msg("Problems with APIs")
        problems_notice = True


def load_redis():
    global actual_enrollers, actual_earned

    redis_enrollers = redis.get("enrollers")
    redis_earned = redis.get("earned")

    if redis_enrollers is not None:
        actual_enrollers = int(redis_enrollers)
    else:
        redis.set("enrollers", actual_enrollers)

    if redis_earned is not None:
        actual_earned = float(redis_earned)
    else:
        redis.set("earned", actual_earned)


load_dotenv()

redis = redis.Redis(host=os.getenv("REDIS_HOST"), port=6379)

cookies = {
    "access_token": os.getenv("ACCESS_TOKEN"),
}

actual_enrollers = 0
actual_earned = 0
problems_notice = False

load_redis()

Timer(300.0, check).start()
