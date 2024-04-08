import json

# BOT TOKEN FILE

TOKEN = open("TOKEN", "r").read()

# BOT CONFIGURATION

DEFAULT_LANGUAGE = "en-EN"
DONATION_MAXIMUM_YEAR = 80 # for example today 2024 year, so the minimum year is 2024 - 80 = 1944

# PostgreSQL Server Configuration

DATABASE_NAME = "crm"
IP_ADDRESS = "108.181.197.188"
PORT = "18384"
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
    (3, "Lviv")
)

REGIONS = (
    (1, "Odes`ka Oblast"),
    (2, "Kiyvska Oblast"),
    (3, "Lvivska Oblast")
)

STREETS = (
    (1, "Generala Petrova, 66"),
    (2, "Akademika Koroliova, 3"),
    (3, "Jopa Bobra, 8"),
    (4, "Abobakar pepe abobakar, 88")
)

AREAS = (
    (1, "Area1"),
    (2, "Area2"),
    (3, "Area3"),
    (4, "Area4"),
    (5, "Area5"),
    (6, "Area6")
)

ADDRESSES = (
    (1, 2, 2, 2, 2, 38),
    (2, 2, 3, 1, 2, 45),
    (3, 1, 1, 1, 1, 78),
    (4, 1, 2, 1, 3, 35),
    (5, 2, 1, 2, 1, 12)
)

STATUSES = (
    (1, "Success"),
    (2, "Unsuccess"),
    (3, "Waiting")
)

CLINICS = (
    (1, "КЛИНИКА АДІН", 1, "8:00:00"),
    (2, "КЛІНІКА ДВА", 2, "12:00:00"),
    (3, "КЛИНИКА ТРИ", 3, "12:00:00"),
    (4, "КЛИНИКА ЧЕТІРЕ", 4, "13:00:00"),
    (5, "КЛИНИКА ПЯТЬ", 5, "14:00:00")
)

GENDERS = (
    (1, "MALE"),
    (2, "FEMALE"),
    (3, "OTHER"),
    (4, "NODATA")
)