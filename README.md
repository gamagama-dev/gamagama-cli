# gamagama

`gamagama` (Game Master Game Manager) is a tool to be used by a Game Master to help run a tabletop RPG. It focuses on the Role Master Unified (RMU) game system.

The core of this repo will be a command-line tool called `gamagama`, or `gg` for short. This tool can be invoked in a interactive "chat" session, to be run "live" while the Game Master (GM) is running a tabletop or online role-playing game.

## Installation

To install the project, run this command from the root directory:

```bash
python3 -m pip install .
```

This creates the `gamagama` and `gg` command-line scripts and makes them available in your shell's path.

## Usage

After installation, you can run the tool using either `gamagama` or `gg`.

To see available options, use the `--help` flag:

```bash
gg --help
```

To start an interactive session, run the command without any arguments:

```bash
gg
```

## Uninstallation

To uninstall the project, run:

```bash
python3 -m pip uninstall gamagama
```

## Contributing

For instructions on how to set up a development environment and run tests, please see [DEVELOPMENT.md](DEVELOPMENT.md).
