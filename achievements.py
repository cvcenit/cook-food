from dataclasses import dataclass
import json

@dataclass
class Achievement:
    key: str
    title: str
    description: str
    unlocked: bool = False

    def unlock(self):
        self.unlocked = True

class AchievementManager:
    SAVE_FILE = "achievements.json"
    
    def __init__(self):
        self._achievements = {
            "first_game":     Achievement("first_game",     "Welcome!",        "Start the game for the first time"),
            "first_kill":     Achievement("first_kill",     "First Blood",     "Kill your first enemy"),
            "first_tower":    Achievement("first_tower",    "Builder",         "Place your first tower"),
            "first_round":    Achievement("first_round",    "Survivor",        "Complete your first round"),
        }
        self._total_kills = 0
        self._total_towers = 0
        self._unlocked = []
        self.load()

    @property
    def achievements(self):
        return self._achievements

    @property
    def unlocked(self):
        return self._unlocked

    def pop_unlocked(self):
        if self.unlocked:
            return self.unlocked.pop(0)
        return None
    
    def _unlock(self, key: str):
        achievement = self._achievements.get(key)
        if achievement and not achievement.unlocked:
            achievement.unlock()
            self.unlocked.append(achievement)
            self.save()

    def on_game_start(self):
        self._unlock("first_game")

    def on_enemy_killed(self):
        self._total_kills += 1
        self._unlock("first_kill")

    def on_tower_placed(self):
        self._total_towers += 1
        self._unlock("first_tower")
    
    def on_round_complete(self):
        self._unlock("first_round")

    def save(self):
        data = {
            "total_kills": self._total_kills,
            "total_towers": self._total_towers,
            "unlocked_keys": [k for k, v in self._achievements.items() if v.unlocked]
        }
        with open(self.SAVE_FILE, "w") as f:
            json.dump(data, f)

    def load(self):
        try:
            with open(self.SAVE_FILE, "r") as f:
                data = json.load(f)
            self._total_kills = data.get("total_kills", 0)
            self._total_towers = data.get("total_towers", 0)
            for key in data.get("unlocked_keys", []):
                if key in self._achievements:
                    self._achievements[key].unlocked = True
        except FileNotFoundError:
            pass

    def reset(self):
        for achievement in self._achievements.values():
            achievement.unlocked = False
        self._total_kills = 0
        self._total_towers = 0
        self._unlocked = []
        self.save()