import argparse


class NoHelpArgumentParser(argparse.ArgumentParser):
    """An ArgumentParser that defaults to not adding a --help argument."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("add_help", False)
        super().__init__(*args, **kwargs)
