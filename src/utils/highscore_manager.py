import os
import json

HIGHSCORE_FILE = "assets/data/highscores.json" # Here is where our json files going to be save.
MAX_SCORES = 10

def load_highscores():
    if not os.path.exists(HIGHSCORE_FILE):
        return []
    with open(HIGHSCORE_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_highscores(highscores):
    with open(HIGHSCORE_FILE, "w") as f:
        json.dump(highscores, f, indent=4)

def try_save_new_score(mode, distance):
    highscores = load_highscores()
    highscores.append({"mode": mode, "distance": round(distance, 1)})

    # Sort descending by distance
    highscores.sort(key=lambda x: x["distance"], reverse=True)

    # Keep only top 5
    highscores = highscores[:MAX_SCORES]
    save_highscores(highscores)

def get_highscore_list():
    return load_highscores()
