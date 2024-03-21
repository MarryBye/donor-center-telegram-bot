import json

# BOT TOKEN FILE

TOKEN = open("TOKEN", "r").read()

# BOT CONFIGURATION

LANG = "uk-UK"
LANG_FILE = json.load(open(f"src/lang/{LANG}.json", "r", encoding="UTF-8"))
MESSAGES_TEXT = LANG_FILE["MESSAGES"]
BUTTONS_TEXT = LANG_FILE["BUTTONS"]

# PostgreSQL Server Configuration

DATABASE_NAME = "crm"
IP_ADDRESS = "163.123.183.82"
PORT = "19980"
USERNAME = "temshik_shemshik"
PASSWORD = "3211234545"