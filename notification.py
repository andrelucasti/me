import os
import requests
from dotenv import load_dotenv


load_dotenv(override=True)


def push_notification(message):
    url = "https://api.pushover.net/1/messages.json"
    data = {
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": message,
        }
    
    requests.post(url, data=data)