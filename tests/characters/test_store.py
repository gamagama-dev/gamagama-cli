import json
from pathlib import Path

from gamagama.characters import CharacterStore


def test_store_load_success(tmp_path):
    char_data = {
        "name": "Frodo",
        "system": "rolemaster",
        "strings": {"race": "Hobbit"},
        "stats": {"strength": 50},
        "skills": {"stealth": 90},
        "counts": {"hit_points": [20, 20]},
    }
    char_file = tmp_path / "frodo.json"
    char_file.write_text(json.dumps(char_data))

    store = CharacterStore(base_dir=tmp_path)
    char = store.load("frodo")

    assert char is not None
    assert char.name == "Frodo"
    assert char.system == "rolemaster"
    assert char.strings == {"race": "Hobbit"}
    assert char.stats == {"strength": 50}
    assert char.skills == {"stealth": 90}
    assert char.counts == {"hit_points": (20, 20)}


def test_store_load_not_found(tmp_path, capsys):
    store = CharacterStore(base_dir=tmp_path)
    char = store.load("nonexistent")

    assert char is None
    captured = capsys.readouterr()
    assert "Character file not found" in captured.out


def test_store_default_base_dir():
    store = CharacterStore()
    expected = Path.home() / ".config" / "gg" / "characters"
    assert store.base_dir == expected
