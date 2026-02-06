# Command Architecture

This document describes the command architecture for Gamagama's CLI interface.

## Core Concepts

### Verb-First Pattern

Commands follow `<verb> [domain] [name]` at root, or just `<verb> [name]` when in a domain context.

### Global Verbs

`show`, `list`, `set`, `load`, `drop` are defined once at root and bubble down to any context. Each domain declares which verbs it supports.

### Active Item

Each domain can have an active item. The active is the default target for verbs, but an explicit name always overrides it.

### Prompt

Shows current path with each domain's active in parentheses:

```
>
player (gandalf)>
system (rolemaster)>
system (rolemaster) schema (player)>
```

## Domain Tree

```
root
├── player (supports: show, list, set, load, drop)
│
└── system (supports: show, list, set)
    └── schema (supports: show, list, set)
```

## Navigation vs Set

| Command | Action | Result |
|---------|--------|--------|
| `set <domain> <name>` | Set active only | Stay at current context |
| `<domain>` | Navigate only | Move to domain, preserve existing active |
| `<domain> <name>` | Navigate + set | Move to domain with active set |

### Examples

```bash
> set player gandalf
>                              # active set, didn't move

> player
player (gandalf)>              # navigated, active was already set

> ..
> player frodo
player (frodo)>                # navigated and changed active in one command

> ..
> player
player (frodo)>                # navigated, active preserved from before
```

**Rule:** `set` is pure (no navigation). Navigation commands optionally accept a name to set active during navigation.

## Global Verbs

| Verb | Arguments | Behavior |
|------|-----------|----------|
| `show` | `[domain] [name]` | Show item details or list of nested actives (see below) |
| `list` | `[domain]` | List all items in domain, mark active with `*` |
| `set` | `[domain] <name>` | Set active item, stay at current context |
| `load` | `[domain] <name>` | Load item from storage (where supported) |
| `drop` | `[domain] [name]` | Remove item, defaults to active (where supported) |

## `show` Behavior

| Context | Nested Actives? | `show` (no args) |
|---------|-----------------|------------------|
| Root | Yes | List all nested actives |
| `system (rolemaster)>` | Yes (schema) | List nested actives (`schema: player`) |
| `system (rolemaster) schema (player)>` | No | Full schema JSON output |
| `player (gandalf)>` | No | Full player details |
| `player>` (no active) | No | "No active player" |

### Rules

1. **Unambiguous context** (no nested actives): Show full details of current active
2. **Ambiguous context** (nested actives exist): Show list of nested actives
3. **Current context's active**: Never in list (already in prompt)
4. **Explicit override**: `show <name>` always shows that item's full details

## Domain Interface

Each domain implements:

```python
class Domain(Protocol):
    supported_verbs: Set[str]

    def list_items(self) -> List[str]
    def get_active(self) -> Optional[str]
    def set_active(self, name: str) -> None
    def show_item(self, name: Optional[str]) -> str
    def has_nested_actives(self) -> bool
    def get_nested_actives(self) -> Dict[str, str]

    # Optional (only if load/drop supported)
    def load_item(self, name: str) -> None
    def drop_item(self, name: Optional[str]) -> None
```

## Session State

```python
@dataclass
class Session:
    system: GameSystem
    active_schema: Optional[str] = None
    players: Dict[str, Character] = field(default_factory=dict)
    active_player: Optional[str] = None
    store: CharacterStore = field(default_factory=CharacterStore)
```

## Example Session

```bash
$ gg
> list system
Available systems:
  generic
  rolemaster

> set system rolemaster
> show
system: rolemaster
player: (none)

> system
system (rolemaster)> list schema
Available schemas:
  character
  creature

> set schema character
system (rolemaster)> show
schema: character

system (rolemaster)> schema
system (rolemaster) schema (character)> show
{ "$schema": "...", "title": "RolemasterCharacter", ... }

system (rolemaster) schema (character)> ..
system (rolemaster)> ..

> load player gandalf
Loaded: gandalf

> load player frodo
Loaded: frodo

> player gandalf
player (gandalf)> show
Name: gandalf
System: rolemaster
Stats:
  co: 85
  ag: 90
  ...

player (gandalf)> show frodo
Name: frodo
System: rolemaster
Stats:
  ...

player (gandalf)> list
  frodo
* gandalf

player (gandalf)> drop
Dropped: gandalf
Active player cleared.

player> set frodo
player (frodo)> ..

> show
system: rolemaster
  schema: character
player: frodo
```

## Help Output

### At Root

```
> help

Navigation:
  player [name]       Manage player characters
  system [name]       Manage game system settings

Commands:
  show [domain] [name]   Show active item or nested actives
  list [domain]          List items in a domain
  set <domain> <name>    Set active item
  load <domain> <name>   Load item from storage
  drop [domain] [name]   Remove item from session

Other:
  help                Show this help
  quit                Exit
```

### In Domain

```
player (gandalf)> help

Current context: player

Commands:
  show [name]         Show player details (default: gandalf)
  list                List loaded players
  set <name>          Set active player
  load <name>         Load player from disk
  drop [name]         Drop player (default: gandalf)

Navigation:
  ..                  Back to root
```

## Unsupported Verb Handling

```bash
system schema> load foo
Error: 'load' is not available in this context
```

## Design Principles

1. **Orthogonal commands:** `set` sets, navigation navigates—never conflated
2. **Active as default:** Verbs use active item when name omitted
3. **Explicit always wins:** Providing a name overrides the active
4. **Context-aware show:** Unambiguous = full details, ambiguous = list actives
5. **Prompt shows state:** Current path + actives visible at a glance
6. **Domains declare verbs:** Only supported verbs available in each context

## Schema System

Schemas are Pydantic models that live in each `GameSystem`. They serve two purposes:

1. **Validation:** gg validates characters on load against the system's schema
2. **Export:** External tools can retrieve JSON Schema via the `show` command

### Schema Registry

```python
class GameSystem:
    schemas: Dict[str, Type[BaseModel]] = {}

    @classmethod
    def get_schema(cls, name: str) -> Optional[dict]:
        model = cls.schemas.get(name)
        return model.model_json_schema() if model else None

    @classmethod
    def list_schemas(cls) -> list[str]:
        return list(cls.schemas.keys())
```

### Example

```python
class RolemasterSystem(GameSystem):
    schemas = {
        "character": RolemasterCharacter,
        "creature": RolemasterCreature,
    }
```
