# Development

This document provides instructions for setting up a development environment to contribute to `gamagama`.

## Setup

This project uses a local Python virtual environment managed via the `Makefile`.

1.  **Install Dependencies**: Run the following command. It will create a virtual environment in `.venv/` if one does not exist, and then install the project and its test dependencies into it.
    ```bash
    make install
    ```

2.  **Activate the Virtual Environment**: To use the tools installed in the virtual environment (like `gg` and `pytest`) directly from your shell, you must activate it.
    *   On macOS and Linux:
        ```bash
        source .venv/bin/activate
        ```
    *   On Windows (PowerShell):
        ```powershell
        .venv\Scripts\Activate.ps1
        ```
    Your shell prompt should change to indicate that the environment is active.

## Running Tests

You can run the test suite using the `make` command, which will automatically use the correct virtual environment:
```bash
make test
```

Alternatively, after activating the virtual environment (see step 2 above), you can run `pytest` directly:
```bash
pytest
```
