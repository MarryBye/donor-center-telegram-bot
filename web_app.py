import asyncio
import redis

from src.classes.WebApp import WebApp
from src.classes.CRMBot import CRMBot

app = WebApp(__name__)

app.config["SECRET_KEY"] = "KluchKotorogoNiktoNeZnaet5"

@app.route("/")
async def index():
    await CRMBot().send_notifications(message="Aboba!")
    return "Разослано"

app.add_url_rule("/", "index", index, methods=["GET", "POST"])