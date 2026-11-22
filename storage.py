# storage.py
# Reads and writes the catalog file (catalog.json).
# This file knows nothing about books or members, it only handles the file.

import json
import os

# Always look for catalog.json next to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CATALOG_PATH = os.path.join(BASE_DIR, "catalog.json")


class StorageError(Exception):
    """Raised when the catalog file cannot be read or saved."""


def load_catalog():
    """Read catalog.json and return its content as a dictionary."""
    try:
        with open(CATALOG_PATH, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        raise StorageError("catalog.json was not found next to the program files")
    except json.JSONDecodeError:
        raise StorageError("catalog.json is damaged or is not valid JSON")
    except OSError as e:
        raise StorageError(f"catalog.json could not be read: {e}")

    # The file must contain a dictionary with a list called "books"
    if not isinstance(data, dict) or not isinstance(data.get("books"), list):
        raise StorageError("catalog.json must contain a list called 'books'")

    # Add the members section if the file does not have it
    if "members" not in data:
        data["members"] = {}
    return data


def save_catalog(data):
    """Write the catalog dictionary to catalog.json."""
    try:
        with open(CATALOG_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except OSError as e:
        raise StorageError(f"The catalog could not be saved: {e}")