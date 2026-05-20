import json

import pytz
from aiogram.client.default import DefaultBotProperties

defaults = DefaultBotProperties(parse_mode="HTML", link_preview_is_disabled=True)
databasePath = "utils/base.db"

defaultTimezone = pytz.timezone("Europe/Moscow")

jsonconf = json.load(open("config.json"))

adminsIds = jsonconf["admins"]

logIgnoreTypes = ["preload"]

nodes = jsonconf["nodes"]


class tokens:
    token = jsonconf["token"]
