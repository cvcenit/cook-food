from achievements import AchievementManager
from graphics import TextButton, TextGraphic
from utils import HEADER_FONT_SIZE, SCREEN_WIDTH

import json

SHOP_ITEMS = [
    {"name": "Extra Life", "cost": 10, "description": "Gain 1 extra life at start"},
    {"name": "Head Start", "cost": 25, "description": "Start with 20 EXP"},
    {"name": "2x Speed", "cost": 30, "description": "Make the game run 2x faster."}
]

SHOP_SAVE_FILE = "./data/shop_data.json"

def load_shop_data() -> dict:
    try:
        with open(SHOP_SAVE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"purchased": []}
    
def save_shop_data(purchased: set):
    with open(SHOP_SAVE_FILE, "w") as f:
        json.dump({"purchased": list(purchased)}, f, indent=4)

def reset_shop_data():
    save_shop_data(set())
        
class ShopModel:
    def __init__(self, achievements: AchievementManager):
        self._achievements = achievements
        self._purchased = set()
        self._screen_change_buttons = [
            TextButton(48, HEADER_FONT_SIZE, "Back", 1)
        ]
        self._items_buttons = [
            TextButton(0, (i + 3) * HEADER_FONT_SIZE, f"{item["name"]} - {item["cost"]} pts", 1)
            for i, item in enumerate(SHOP_ITEMS)
        ]
        self._reset_buttons = [
            TextButton(48, HEADER_FONT_SIZE * 2, "Reset Shop", 8)
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
        if index in self._purchased:
            self._message = f"Already purchased: {item['name']}"
            return
        if self._achievements.spend_points(item["cost"]):
            self._purchased.add(index)
            save_shop_data(self._purchased)
            self._message = f"Purchased: {item['name']}"
        else:
            self._message = "Not enough points!"
    
    def reset_purchases(self):
        self._purchased = set()
        reset_shop_data()
        self._message = "Shop reset!"

    def start_screen(self):
        self._message = ""
        data = load_shop_data()
        self._purchased = set(data.get("purchased", []))

    def reset(self):
        self.start_screen()

    def update(self, clicked_idx):
        pass