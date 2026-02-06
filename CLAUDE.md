# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Test Commands

```bash
make install                # Create .venv and install in editable mode with test deps
source .venv/bin/activate   # Activate venv (required for pytest/gg directly)
pytest                      # Run all tests (fast, requires activated venv)
pytest tests/commands/      # Run a specific test directory
pytest tests/test_main.py::test_name  # Run a single test
make test                   # Safe: ensures venv + deps before running pytest
```

## Architecture

Gamagama is a dual-mode CLI tool (`gg`): it runs either as a one-shot CLI (when args are provided) or as an interactive REPL (when launched with no args). Both modes share the same command tree and session injection.

### Core Flow

`core/main.py:run()` loads TOML config, resolves the game system (CLI arg > config > "generic" default), builds the `CommandTree`, then dispatches to `run_cli_mode` or `run_interactive_mode`.

### Command System

Commands are auto-discovered. To add one, create a module under `src/gamagama/commands/` with a class that inherits `CommandBase`:
- `name`: command identifier
- `path`: list of parent branch names (e.g., `["system"]` nests it under the `system` branch)
- `setup(spec)`: call `spec.add_argument()` to define args (stored, applied to argparse later)
- `handle(args)`: execution logic; `args._session` provides the Session, `args._interactive` is a bool

Commands are registered into a `CommandTree` (extends `Tree`) as `CommandSpec` leaf nodes. In CLI mode, `ArgparseBuilder` (visitor pattern) walks the tree to build an argparse subparser hierarchy. In interactive mode, commands are resolved via bubbling lookup (walks up from current node) then strict downward traversal.

### Tree Structure (`core/tree/`)

Generic hierarchical tree with two branch types:
- `MapBranch`: named children (dict), used for command namespaces
- `SeqBranch`: ordered children (list), for sequence data

The `NodeVisitor` base class dispatches via `visit_ClassName()` reflection.

### Game Systems (`systems/`)

`SYSTEMS` dict in `systems/__init__.py` maps names to `GameSystem` subclasses. Each system owns a `DiceEngine` subclass. The Rolemaster engine implements open-ended rolls (96-100 explode up, 01-05 explode down). Add new systems by subclassing `GameSystem` and `DiceEngine`, then registering in `SYSTEMS`.

### Session

`Session` holds the current tree position, active `GameSystem` instance, and exit flag. It is injected into command args as `_session`.
