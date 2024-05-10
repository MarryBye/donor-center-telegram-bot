import os
import json

LANGUAGES = {}

for language_file in os.listdir("src/lang/"):
    if language_file.endswith(".json"):
        language = language_file.replace(".json", "")
        LANGUAGES[language] = json.load(open(f"src/lang/{language_file}", "r", encoding="UTF-8"))
