from src.classes.Keyboards import Keyboard, KeyboardController, KeyboardName
from src.classes.Controllers.DatabaseController import DatabaseController

kb = KeyboardController()
db = DatabaseController()

regions = db.get_regions()

kb_scheme = []

kb_scheme_row = []
for i, region in enumerate(regions, start=0):
    kb_scheme_row.append({region.get_region_name(): {"callback_data": str(region.get_id())}})
    if i % 3 == 0 or i >= len(regions) - 1:
        kb_scheme.append(kb_scheme_row)
        kb_scheme_row = []

cities = db.get_cities()

kb_scheme = []

kb_scheme_row = []
for i, city in enumerate(cities, start=0):
    kb_scheme_row.append({city.get_city_name(): {"callback_data": str(city.get_id())}})
    if i % 3 == 0 or i >= len(cities) - 1:
        kb_scheme.append(kb_scheme_row)
        kb_scheme_row = []

keyboard = Keyboard(keyboard_scheme=kb_scheme, need_translation=False)
kb.add_keyboard(keyboard_name=KeyboardName.REGIONS, keyboard=keyboard)
