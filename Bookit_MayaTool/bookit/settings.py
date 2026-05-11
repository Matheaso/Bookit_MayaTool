import json
import os
from dataclasses import dataclass, asdict
from maya import cmds

@dataclass
class BookitSettings:
    seed: int = 1
    random_seed: bool = True
    rotate: bool = True
    auto_select: bool = False
    delete_percent: int = 0
    rotation_value: int = 0
    auto_save_on_exit_button: bool = False

def get_settings_path():
    folder = os.path.join(cmds.internalVar(userAppDir=True), 'bookit')
    os.makedirs(folder, exist_ok=True)

    return os.path.join(folder, 'settings.json')

def load_settings() -> BookitSettings:
    path = get_settings_path()

    if not os.path.exists(path):
        return BookitSettings()

    try:
        with open(path, 'r') as file:
            data = json.load(file)

            default_data = asdict(BookitSettings())
            default_data.update(data)

            return BookitSettings(**default_data)

    except Exception as error:
        cmds.warning(f"Could not load Bookit settings: {error}")
        return BookitSettings()


def save_settings(settings: BookitSettings):
    path = get_settings_path()

    try:
        with open(path, 'w') as file:
            json.dump(asdict(settings), file, indent=4)

    except Exception as error:
        cmds.warning(f"Could not save Bookit settings: {error}")

def delete_settings():
    path = get_settings_path()

    if os.path.exists(path):
        os.remove(path)