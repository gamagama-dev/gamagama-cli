# gamagama

`gamagama` (Game Master Game Manager) is a tool to be used by a Game Master to help run a tabletop RPG. It focuses on the Role Master Unified (RMU) game system.

The core of this repo will be a command-line tool called `gamagama`, or `gg` for short. This tool can be invoked in a interactive "chat" session, to be run "live" while the Game Master (GM) is running a tabletop or online role-playing game.

## Installation

### For Development

To install the project for development, run the following command from the root directory of the repository:

```bash
python3 -m pip install -e .
```

This performs an "editable" install, which means that any changes you make to the source code will be immediately available when you run the tool, without needing to reinstall.

### For Regular Use

To install the project for regular use, run this command from the root directory:

```bash
python3 -m pip install .
```

Both installation methods create the `gamagama` and `gg` command-line scripts and makes them available in your shell's path.

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
