# Development

This document provides instructions for setting up a development environment to contribute to `gamagama`.

## Setup

1.  **Install in Editable Mode**: To install the project for development, run the following command from the root directory of the repository. This allows you to edit the source code and have the changes immediately reflected in your installed version.

    ```bash
    python3 -m pip install -e .
    ```

2.  **Install Test Dependencies**: The project uses `pytest` for testing. To install it, run:

    ```bash
    python3 -m pip install -e '.[test]'
    ```

## Running Tests

After setting up the environment, you can run the entire test suite with this command:

```bash
pytest
```
