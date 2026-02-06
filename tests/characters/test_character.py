from gamagama.characters import Character


def test_character_defaults():
    char = Character(name="Test")
    assert char.name == "Test"
    assert char.system == "generic"
    assert char.strings == {}
    assert char.stats == {}
    assert char.skills == {}
    assert char.counts == {}


def test_character_from_dict_minimal():
    data = {"name": "Gandalf"}
    char = Character.from_dict(data)
    assert char.name == "Gandalf"
    assert char.system == "generic"


def test_character_from_dict_full():
    data = {
        "name": "Gandalf",
        "system": "rolemaster",
        "strings": {
            "player": "Dave",
            "race": "Istari",
        },
        "stats": {
            "strength": 75,
            "agility": 60,
        },
        "skills": {
            "channeling": 85,
            "perception": 70,
        },
        "counts": {
            "hit_points": [25, 45],
            "power_points": [12, 30],
        },
    }
    char = Character.from_dict(data)

    assert char.name == "Gandalf"
    assert char.system == "rolemaster"
    assert char.strings == {"player": "Dave", "race": "Istari"}
    assert char.stats == {"strength": 75, "agility": 60}
    assert char.skills == {"channeling": 85, "perception": 70}
    assert char.counts == {"hit_points": (25, 45), "power_points": (12, 30)}
