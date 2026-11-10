import os

from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# BOT TOKEN CONFIGURATION
# Reads from BOT_TOKEN environment variable with a safe development fallback
BOT_TOKEN = os.getenv("BOT_TOKEN", "123456789:ABCdefGHIjklMNOpqrsTUVwxyz")
TOKEN = BOT_TOKEN  # Backwards compatibility alias

# BOT CONFIGURATION
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "en-EN")
NEED_DEBUG = os.getenv("NEED_DEBUG", "True").strip().lower() in ("true", "1", "yes")

# POSTGRESQL SERVER CONFIGURATION
# Reads from environment variables with sensible defaults
DATABASE_NAME = os.getenv("DATABASE_NAME") or os.getenv("POSTGRES_DB") or "crm"
IP_ADDRESS = os.getenv("IP_ADDRESS") or os.getenv("POSTGRES_HOST") or "localhost"
PORT = os.getenv("PORT") or os.getenv("POSTGRES_PORT") or "5432"
USERNAME = os.getenv("DB_USER") or os.getenv("POSTGRES_USER") or "postgres"
DB_PASSWORD = os.getenv("DB_PASSWORD") or os.getenv("POSTGRES_PASSWORD") or "postgres"
PASSWORD = DB_PASSWORD  # Backwards compatibility alias

# Database integration

BLOODS = (
    (1, "AB+"),
    (2, "AB-"),
    (3, "A+"),
    (4, "A-"),
    (5, "B+"),
    (6, "B-"),
    (7, "O+"),
    (8, "O-"),
)

LANGUAGES = (
    (1, "cn-CN"),
    (2, "de-DE"),
    (3, "en-EN"),
    (4, "fr-FR"),
    (5, "ru-RU"),
    (6, "uk-UK"),
)

CITIES = (
    (1, "Odessa"),
    (2, "Kiyv"),
    (3, "Lviv"),
    (4, "Kharkiv"),
)

REGIONS = (
    (1, "Odessa"),
    (2, "Kyiv"),
    (3, "Lviv"),
    (4, "Kharkiv"),
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
    (3, "Waiting"),
)

CLINICS = (
    (1, "Odesa Center #1", 1, "8:00:00"),
    (2, "Kiyv Center #1' mall", 2, "9:00:00"),
)

GENDERS = (
    (1, "MALE"),
    (2, "FEMALE"),
    (3, "OTHER"),
    (4, "NODATA"),
)

ADMINS = (
    (1, "SuperAdminC1", "qwerty", 1),
    (2, "SuperAdminC2", "qwerty", 2),
)
