from achievements import AchievementManager
from graphics import TextButton, TextGraphic
from utils import HEADER_FONT_SIZE, SCREEN_WIDTH, CONTENT_FONT_SIZE, CONTENT_FONT, CONTENT_FONT_PATH

SHOP_ITEMS = [
    {"name": "Extra Life", "cost": 10, "description": "Gain 1 extra life at start"},
    {"name": "Head Start", "cost": 25, "description": "Start with 20 EXP"},
    {"name": "2x Speed", "cost": 30, "description": "Make the game run 2x faster."}
]

class ShopModel:
    def __init__(self, achievements: AchievementManager):
        self._achievements = achievements
        self._purchased = set()
        self._screen_change_buttons = [
            TextButton(48, HEADER_FONT_SIZE, "Back", 5)
        ]
        self._items_buttons = [
            TextButton(0, (i + 6) * (CONTENT_FONT_SIZE + 16), f"{item["name"]} - {item["cost"]} pts", 1, font_path=CONTENT_FONT_PATH, size=48)
            for i, item in enumerate(SHOP_ITEMS)
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
    
    def buy(self, index: int):
        item = SHOP_ITEMS[index]
        if index in self._purchased:
            self._message = f"Already purchased: {item["name"]}"
            return
        if self._achievements.points >= item["cost"]:
            self._achievements.spend_points(item["cost"])
            self._purchased.add(index)
            self._message = f"Purchased: {item["name"]}"
        else:
            self._message = "Not enough points!"
    
    def start_screen(self):
        self._message = ""

    def reset(self):
        self.start_screen()

    def update(self, clicked_idx):
        pass