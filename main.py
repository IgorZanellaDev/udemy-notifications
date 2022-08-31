from pprint import pprint
import requests
from dotenv import load_dotenv
import os

load_dotenv()

cookies = {
    "access_token": os.getenv("ACCESS_TOKEN"),
}

enrollers = requests.get("https://www.udemy.com/api-2.0/instructor-performance/enrollment-metrics/?fields[user]=total,current_month,daily,monthly", cookies=cookies)

total = requests.get("https://www.udemy.com/api-2.0/share-holders/v1.0/371956/total/?timeframe=month&aggregate=day&breakdown=revenue_type", cookies=cookies)

pprint(enrollers.text)
pprint(total.text)