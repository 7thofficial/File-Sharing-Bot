import os
import string
import random
import pytz
from datetime import date, timedelta
import requests as re

SHORTNER_URL = os.environ.get("SHORTNER_URL")
SHORTNER_API = os.environ.get("SHORTNER_API")

async def get_shortlink(link):
    res = re.get(f'https://{SHORTNER_URL}/api?api={SHORTNER_API}&url={link}')
    res.raise_for_status()
    data = res.json()
    return data.get('shortenedUrl')

TOKENS = {}
VERIFIED = {}

async def generate_random_string(num: int):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(num))
    return random_string

async def check_token(bot, userid, token):
    user = await bot.get_users(userid)
    if user.id in TOKENS:
        TKN = TOKENS[user.id]
        if token in TKN:
            is_used = TKN[token]
            return not is_used
    return False

async def get_token(bot, userid, link):
    user = await bot.get_users(userid)
    token = await generate_random_string(7)
    TOKENS[user.id] = {token: False}
    link = f"{link}verify-{user.id}-{token}"
    shortened_verify_url = await get_shortlink(link)
    return str(shortened_verify_url)

async def verify_user(bot, userid, token):
    user = await bot.get_users(userid)
    TOKENS[user.id] = {token: True}
    tz = pytz.timezone('Asia/Kolkata')
    today = date.today()
    VERIFIED[user.id] = today

async def check_verification(bot, userid):
    user = await bot.get_users(userid)
    tz = pytz.timezone('Asia/Kolkata')
    today = date.today()
    if user.id in VERIFIED:
        last_verified = VERIFIED[user.id]
        cooldown_period = timedelta(days=1)  # 24 hours cooldown
        return (today - last_verified) >= cooldown_period
    return False
