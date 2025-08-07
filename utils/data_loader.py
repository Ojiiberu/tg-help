import json

def load_commands():
    with open("data/commands.json", encoding="utf-8") as f:
        return json.load(f)
    
def get_command_info(name: str):
    commands = load_commands()
    return commands.get(name.lower())