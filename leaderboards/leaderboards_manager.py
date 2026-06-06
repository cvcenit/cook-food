import json

PLAYER_DATA_PATH = "data/player_data.json"

def load_data() -> dict:
    try:
        with open(PLAYER_DATA_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    
def save_data(data: dict):
    with open(PLAYER_DATA_PATH, "w") as f:
        json.dump(data, f, indent=4)

def save_player(name: str, rounds: int, mode: str):
    data = load_data()
    if name not in data:
        data[name] = {
            "name": name,
            "campaign_completed_levels": [],
            "campaign_completed_rounds": 0,
            "endless_highest_rounds": 0
        }

    if mode == "endless":
        data[name]["endless_highest_rounds"] = max(data[name]["endless_highest_rounds"], rounds)
    else:
        data[name]["campaign_completed_rounds"] = max(data[name]["campaign_completed_rounds"], rounds)

    save_data(data)

def register_player(name: str, rounds: int, mode: str) -> str:
    if not name or name == "Enter your name":
        return ""
    save_player(name, rounds, mode)
    return "Registered!"