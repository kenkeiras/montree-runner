import json
import os

CONFIG_PATH = os.path.expanduser("~/.config/montree-runner/config.json")
DEFAULT_ROOT_URL = "https://montree.spiral.systems"

def has_configuration():
    return os.path.exists(CONFIG_PATH)


def get_configuration():
    with open(CONFIG_PATH, 'rb') as f:
        return json.load(f)


def run_first_time_configuration():
    root_url = input("Root url [{}]: ".format(DEFAULT_ROOT_URL)) or DEFAULT_ROOT_URL
    project_id = ""
    while len(project_id.strip()) < 1:
        project_id = input("Project ID: ")

    api_key = input("Cookie: ")

    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, 'wt') as f:
        json.dump({
            "root_url": root_url,
            "project_id": project_id,
            "cookie": api_key,
        }, f, indent=4)
