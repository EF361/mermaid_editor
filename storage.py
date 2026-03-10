import json
import os
import uuid

STORAGE_DIR = "diagrams"

os.makedirs(STORAGE_DIR, exist_ok=True)


def new_diagram():

    diagram_id = str(uuid.uuid4())

    data = {
        "id": diagram_id,
        "title": "Untitled Diagram",
        "code": """flowchart TD
A[Start] --> B[Write Mermaid Code]
B --> C[Preview Diagram]
"""
    }

    path = f"{STORAGE_DIR}/{diagram_id}.json"

    with open(path, "w") as f:
        json.dump(data, f)

    return diagram_id


def save_diagram(id, title, code):

    path = f"{STORAGE_DIR}/{id}.json"

    data = {
        "id": id,
        "title": title,
        "code": code
    }

    with open(path, "w") as f:
        json.dump(data, f)


def load_diagram(id):

    path = f"{STORAGE_DIR}/{id}.json"

    if not os.path.exists(path):
        return {
            "id": id,
            "title": "Untitled Diagram",
            "code": ""
        }

    with open(path) as f:
        return json.load(f)


def list_diagrams():

    diagrams = []

    for file in os.listdir(STORAGE_DIR):

        with open(f"{STORAGE_DIR}/{file}") as f:
            diagrams.append(json.load(f))

    return diagrams