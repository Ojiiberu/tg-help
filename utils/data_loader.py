import json
from typing import Dict
import random

def load_commands() -> Dict[str, dict]:
    with open("data/commands.json", encoding="utf-8") as f:
        return json.load(f)
    
def get_command_info(name: str):
    commands = load_commands()
    if not commands: return None
    return commands.get(name.lower())

def get_category(category: str) -> Dict[str, dict]:
    commands = load_commands()
    if not commands: return None
    norm = (category or "").strip().casefold()
    result = {}
    for name, data in commands.items():
        cat = str(data.get("category", "")).strip().casefold()
        if cat == norm:
            result[name] = data
    return result

def get_all_categories() -> list:
    commands =  load_commands()
    if not commands: return None
    cats = {str(v.get("category", "")).strip() for v in commands.values() if v.get("category")}
    return sorted(cats)

def random_command():
    commands = load_commands()
    if not commands: return None
    cmd_name = random.choice(list(commands.keys()))
    cmd_data = commands[cmd_name]
    return {"name": cmd_name, **cmd_data}
