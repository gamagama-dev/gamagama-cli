from .base import GameSystem
from .generic import GenericSystem
from .rolemaster import RolemasterSystem

SYSTEMS = {
    "generic": GenericSystem,
    "rolemaster": RolemasterSystem,
}
