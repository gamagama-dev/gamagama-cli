from importlib.metadata import entry_points
from gamagama.core import GameSystem
from .generic import GenericSystem


def load_systems():
    systems = {"generic": GenericSystem}
    for ep in entry_points(group="gamagama.systems"):
        systems[ep.name] = ep.load()
    return systems


SYSTEMS = load_systems()
