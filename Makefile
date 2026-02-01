# Define the virtual environment directory and the Python interpreter within it.
VENV_DIR := .venv
VENV_PYTHON := $(VENV_DIR)/bin/python

# Set the default goal to 'help'
.DEFAULT_GOAL := help

# Phony targets are rules that don't represent files.
.PHONY: help install uninstall test clean serve-docs build-docs

help:
	@echo "Available commands:"
	@echo "  install     - Create a virtual environment and install the project in editable mode."
	@echo "  test        - Run tests using pytest."
	@echo "  serve-docs  - Install doc dependencies and serve the documentation locally."
	@echo "  build-docs  - Install doc dependencies and build static HTML documentation."
	@echo "  uninstall   - Remove the virtual environment and cached files."
	@echo "  clean       - Remove all build artifacts, caches, and the virtual environment."

# This rule depends on the virtual environment's Python executable existing.
# If it doesn't, make will run the rule to create it first.
install: $(VENV_PYTHON)
	@echo "Installing project in editable mode with test dependencies..."
	@$(VENV_PYTHON) -m pip install -e '.[test]'

# This rule runs pytest using the virtual environment's interpreter.
# We depend on 'install' to ensure the package is installed in editable mode,
# which is required for Python to find the package in the 'src' directory.
test: install
	$(VENV_PYTHON) -m pytest

# Install documentation dependencies and serve the site
serve-docs: $(VENV_PYTHON)
	@echo "Installing documentation dependencies..."
	@$(VENV_PYTHON) -m pip install -e '.[docs]'
	@echo "Serving documentation at http://127.0.0.1:8000"
	@$(VENV_PYTHON) -m mkdocs serve

# Build the static HTML documentation without serving it
build-docs: $(VENV_PYTHON)
	@echo "Building documentation..."
	@$(VENV_PYTHON) -m pip install -e '.[docs]'
	@$(VENV_PYTHON) -m mkdocs build
	@echo "Build complete. Open site/index.html to view."

# This rule removes the virtual environment and cached files.
uninstall:
	rm -rf $(VENV_DIR)
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +

# This rule cleans everything that 'uninstall' does, plus build artifacts.
clean: uninstall
	rm -rf build/
	find . -type d -name "*.egg-info" -exec rm -r {} +

# This is a helper rule that creates the virtual environment if it's missing.
# The 'install' rule depends on its target file.
$(VENV_PYTHON):
	@echo "Creating virtual environment in $(VENV_DIR) and upgrading dependencies..."
	@echo "This may take a few moments. Please be patient."
	@python3 -m venv --upgrade-deps $(VENV_DIR) < /dev/null
	@echo "Virtual environment created."
	@echo "To activate it, run: source $(VENV_DIR)/bin/activate"
	@echo "To deactivate it, run: deactivate"
