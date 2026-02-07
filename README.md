# gamagama-cli

`gamagama-cli` (Game Master Game Manager — CLI) is a tool to be used by a Game Master to help run a tabletop RPG. It focuses on the Role Master Unified (RMU) game system.

The core of this repo is a command-line tool called `gg-cli`. This tool can be invoked in a interactive "chat" session, to be run "live" while the Game Master (GM) is running a tabletop or online role-playing game.

## Installation

The recommended way to install `gamagama-cli` is using `pipx`, which automatically handles virtual environments.

1.  **Install pipx**: If you don't have it, install `pipx` first.
    ```bash
    python3 -m pip install --user pipx
    python3 -m pipx ensurepath
    ```
    You may need to open a new terminal for the path changes to take effect.

2.  **Install gamagama-cli**: From the project's root directory, run:
    ```bash
    pipx install .
    ```

This installs the tool in an isolated environment and makes the `gg-cli` command available system-wide.

## Usage

After installation, you can run the tool using `gg-cli`.

To see available options, use the `--help` flag:

```bash
gg-cli --help
```

To start an interactive session, run the command without any arguments:

```bash
gg-cli
```

## Uninstallation

If you installed the project with `pipx`, run:

```bash
pipx uninstall gamagama-cli
```

## Contributing

For instructions on how to set up a development environment and run tests, please see [DEVELOPMENT.md](DEVELOPMENT.md).
