import json


# Save Data As Json File In Given Path
def save_to_json(data: dict, filepath: str) -> None:
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii="False")


# Load Json
def load_json(path: str):
    with open(path) as file:
        data = json.load(file)
        return data
