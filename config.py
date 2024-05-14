# BOT TOKEN FILE

TOKEN = open("TOKEN", "r").read()

# BOT CONFIGURATION

DEFAULT_LANGUAGE = "en-EN"

# PostgresSQL Server Configuration

DATABASE_NAME = "crm"
IP_ADDRESS = "108.181.197.190"
PORT = "19008"
USERNAME = "temshik_shemshik"
PASSWORD = "3211234545"

# Database integration

BLOODS = (
    (1, "AB+"),
    (2, "AB-"),
    (3, "A+"),
    (4, "A-"),
    (5, "B+"),
    (6, "B-"),
    (7, "O+"),
    (8, "O-")
)

LANGUAGES = (
    (1, "cn-CN"),
    (2, "de-DE"),
    (3, "en-EN"),
    (4, "fr-FR"),
    (5, "ru-RU"),
    (6, "uk-UK")
)

CITIES = (
    (1, "Odessa"),
    (2, "Kiyv"),
    (3, "Lviv"),
    (4, "Kharkiv")
)

REGIONS = (
    (1, "Odessa"),
    (2, "Kyiv"),
    (3, "Lviv"),
    (4, "Kharkiv")
)

STREETS = (
    (1, "Klochkivska"),
    (2, "Pushkin's"),
)

AREAS = (
    (1, "Shevchenkivskyi"),
    (2, "Kyivіkyi"),
)

ADDRESSES = (
    (1, 1, 1, 1, 1, 366),
    (2, 2, 2, 2, 2, 24),
)

STATUSES = (
    (1, "Success"),
    (2, "Unsuccess"),
    (3, "Waiting")
)

CLINICS = (
    (1, "Odesa Center #1", 1, "8:00:00"),
    (2, "Kiyv Center #1' mall", 2, "9:00:00"),
)

GENDERS = (
    (1, "MALE"),
    (2, "FEMALE"),
    (3, "OTHER"),
    (4, "NODATA")
)
