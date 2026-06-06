from achievements.achievements_manager import AchievementManager
from graphics import TextButton, TextGraphic
from utils import HEADER_FONT_SIZE, SCREEN_WIDTH, CONTENT_FONT_SIZE, CONTENT_FONT, CONTENT_FONT_PATH

import json

SHOP_ITEMS = [
    {"name": "Extra Life", "cost": 5, "description": "Gain 1 extra life at start", "repeatable": True},
    {"name": "Head Start", "cost": 10, "description": "Start with 20 EXP", "repeatable": False},
    {"name": "2x Speed", "cost": 10, "description": "Make the game run 2x faster.", "repeatable": False}
]

SHOP_SAVE_FILE = "./data/shop_data.json"

def load_shop_data() -> dict:
    try:
        with open(SHOP_SAVE_FILE, "r") as f:
            return json.load(f)
        purchased = data.get("purchased", {})
        if isinstance(purchased, list):
            purchased = {str(i): 1 for i in purchased}
        return {"purchased": purchased}
    except FileNotFoundError:
        return {"purchased": {}}
    
def save_shop_data(purchased: dict):
    with open(SHOP_SAVE_FILE, "w") as f:
        json.dump({"purchased": purchased}, f, indent=4)
        
def reset_shop_data():
    save_shop_data({})
        
class ShopModel:
    def __init__(self, achievements: AchievementManager):
        self._achievements = achievements
        data = load_shop_data()
        self._purchased = data.get("purchased", {})
        self._screen_change_buttons = [
            TextButton(48, HEADER_FONT_SIZE, "Back", 10, size=38)
        ]
        self._items_buttons = [
            TextButton(0, (i + 5) * (CONTENT_FONT_SIZE - 30), f"{item["name"]} - {item["cost"]} pts", 1, font_path=CONTENT_FONT_PATH, size=84)
            for i, item in enumerate(SHOP_ITEMS)
        ]
        self._reset_buttons = [
            TextButton(48, HEADER_FONT_SIZE * 2, "Reset Shop", 3, size=35)
        ]
        for button in self._items_buttons:
            _, y = button.current_position
            button.change_position(SCREEN_WIDTH / 2 - button.width / 2, y)
        
        self._message = ""

    @property
    def screen_change_buttons(self):
        return self._screen_change_buttons
    
    @property
    def item_buttons(self):
        return self._items_buttons
    
    @property
    def message(self):
        return self._message
    
    @property
    def purchased(self):
        return self._purchased
    
    @property
    def reset_buttons(self):
        return self._reset_buttons
    
    def buy(self, index: int):
        item = SHOP_ITEMS[index]
        key = str(index)
        if not item.get("repeatable", False) and key in self._purchased:
            self._message = f"Already purchased: {item['name']}"
            return
        if self._achievements.spend_points(item["cost"]):
            self._purchased[key] = self._purchased.get(key, 0) + 1
            save_shop_data(self._purchased)
            self._message = f"Purchased: {item['name']}"
        else:
            self._message = "Not enough points!"
    
    def reset_purchases(self):
        self._purchased = {}
        reset_shop_data()
        self._message = "Shop reset!"

    def start_screen(self):
        self._message = ""
        data = load_shop_data()
        self._purchased = data.get("purchased", {})

    def reset(self):
        self.start_screen()

    def update(self, clicked_idx):
        pass