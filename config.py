# BOT TOKEN FILE

TOKEN = open("TOKEN", "r").read()

# BOT CONFIGURATION

DEFAULT_LANGUAGE = "en-EN"
DONATION_MAXIMUM_YEAR = 80  # for example today 2024 year, so the minimum year is 2024 - 80 = 1944

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
    (1, 1, 4, 4, 1, 366),
    (2, 2, 4, 4, 2, 2),
)

STATUSES = (
    (1, "Success"),
    (2, "Unsuccess"),
    (3, "Waiting")
)

CLINICS = (
    (1, "Blood center in Kharkiv", 1, "Mon-Fri 08:00-15:00 / Sat 08:00-13:00"),
    (2, "blood center in 'Nikolskyi' mall", 2, "Tue, Thu, Sat 09:00-14:00"),
)

GENDERS = (
    (1, "MALE"),
    (2, "FEMALE"),
    (3, "OTHER"),
    (4, "NODATA")
)
