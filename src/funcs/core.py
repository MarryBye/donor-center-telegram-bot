from src.lang.languages import LANGUAGES

def get_multilang_button(key: str) -> list:
    command_variations = []
    for language in LANGUAGES:
        command_variations.append(LANGUAGES[language]["BUTTONS"][key])
    return command_variations