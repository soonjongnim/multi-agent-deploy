import requests
import os

SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK")
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

def send_slack(message):
    if SLACK_WEBHOOK:
        requests.post(SLACK_WEBHOOK, json={"text": message})

def send_discord(message):
    if DISCORD_WEBHOOK:
        requests.post(DISCORD_WEBHOOK, json={"content": message})
