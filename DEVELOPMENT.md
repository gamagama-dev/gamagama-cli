# Development

This document provides instructions for setting up a development environment to contribute to `gamagama`.

## Setup

It is highly recommended to use a Python virtual environment to isolate project dependencies.

1.  **Create a Virtual Environment**: From the root directory, create a new virtual environment. A common convention is to name it `.venv`.

    ```bash
    python3 -m venv .venv
    ```

2.  **Activate the Virtual Environment**: Before installing dependencies, you must activate the environment.

    *   On macOS and Linux:
        ```bash
        source .venv/bin/activate
        ```
    *   On Windows (PowerShell):
        ```powershell
        .venv\Scripts\Activate.ps1
        ```

    Your shell prompt should change to indicate that you are in the active environment.

3.  **Install Dependencies**: With the virtual environment active, install the project in "editable" mode along with its test dependencies using a single command:

    ```bash
    python3 -m pip install -e '.[test]'
    ```

## Running Tests

After setting up the environment, you can run the entire test suite with this command:

```bash
pytest
```
