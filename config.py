import json

TOKEN = open("TOKEN", "r").read()

LANG = "uk-UK"
LANG_FILE = json.load(open(f"src/lang/{LANG}.json", "r", encoding="UTF-8"))
MESSAGES_TEXT = LANG_FILE["MESSAGES"]
BUTTONS_TEXT = LANG_FILE["BUTTONS"]