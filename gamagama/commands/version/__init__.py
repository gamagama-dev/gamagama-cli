from importlib.metadata import version, PackageNotFoundError
from ..base import CommandBase


class VersionCommand(CommandBase):
    """Displays the application version."""

    name = "version"
    help = "Displays the application version."

    def setup(self, spec):
        pass

    def handle(self, args):
        try:
            v = version("gamagama")
            print(f"gamagama v{v}")
        except PackageNotFoundError:
            print("gamagama version unknown (package not installed)")
